"""Launch the Remote Eval server in a Modal Sandbox.

Setup and usage are documented in README.md. Run with:
    uv run python modal/modal_remote_eval.py
"""

import argparse
from pathlib import Path

import modal


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-name", default="learn-bt-remote-eval")
    parser.add_argument("--secret-name", default="learn-bt-remote-eval")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    image = (
        modal.Image.debian_slim(python_version="3.12")
        .apt_install("curl", "ca-certificates")
        .env({
            "PATH": "/opt/venv/bin:/root/.local/bin:/root/.cargo/bin:"
                    "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "UV_PROJECT_ENVIRONMENT": "/opt/venv",
            "BASE_URL": "https://gateway.braintrust.dev",
            "PYTHONUNBUFFERED": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        })
        # Use the standalone bt CLI, matching the workshop's local server.
        .run_commands(
            "curl -fsSL https://github.com/braintrustdata/bt/releases/download/"
            "v0.29.0/bt-installer.sh -o /tmp/install-bt.sh",
            "sh /tmp/install-bt.sh --no-modify-path",
            "bt --version",
        )
        .pip_install("uv==0.12.11")
        .workdir("/app")
        .add_local_file(root / "pyproject.toml", "/app/pyproject.toml", copy=True)
        .add_local_file(root / "uv.lock", "/app/uv.lock", copy=True)
        .run_commands("uv sync --frozen --no-dev --no-install-project --no-cache")
        # Only upload the source needed by the server; .env stays local.
        .add_local_dir(
            root / "agent",
            "/app/agent",
            copy=True,
            ignore=["**/__pycache__", "**/*.pyc", ".env", ".env.*"],
        )
        .add_local_file(
            root / "evals/eval_agent_remote_server.py",
            "/app/evals/eval_agent_remote_server.py",
            copy=True,
        )
    )

    with modal.enable_output():
        app = modal.App.lookup(args.app_name, create_if_missing=True)
        sandbox = modal.Sandbox.create(
            "bt", "eval", "evals/eval_agent_remote_server.py",
            "--runner", "/opt/venv/bin/python",
            "--dev", "--dev-host", "0.0.0.0", "--dev-port", "8300",
            app=app,
            image=image,
            secrets=[
                modal.Secret.from_name(
                    args.secret_name,
                    required_keys=["BRAINTRUST_API_KEY", "BASE_URL"],
                )
            ],
            encrypted_ports=[8300],
            readiness_probe=modal.Probe.with_tcp(8300),
            timeout=3600,
            cpu=1,
            memory=1024,
        )
        print(f"Sandbox ID: {sandbox.object_id}", flush=True)
        try:
            sandbox.wait_until_ready(timeout=120)
            url = sandbox.tunnels()[8300].url
        except BaseException:
            sandbox.terminate()
            raise

    print(f"Remote Eval URL: {url}")
    print("Register this URL in Braintrust → Settings → Remote Evals.")
    print("The sandbox runs independently for up to one hour.")
    print(f"Stop early: uv run modal sandbox terminate {sandbox.object_id}")


if __name__ == "__main__":
    main()
