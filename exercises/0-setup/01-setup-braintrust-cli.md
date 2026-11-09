# 0.1 Set up the local environment [CLI]

Lets start by setting up this local environment. The API key authorizes this codebase to send traces and create resources within a Braintrust org, using permissions associated with your account in that organization.

## Step 1: Install the project dependencies

From the repository root, run:

```bash
uv sync
```

This creates a local virtual environment and installs the app, Braintrust SDK,
and CLI dependencies used in the exercises.

## Step 2: Create your local environment file

Create a private `.env` file from the template:

```bash
cp example.env .env
```

Open `.env` and replace the placeholders.

```dotenv
BRAINTRUST_API_KEY=your-api-key
BASE_URL=https://gateway.braintrust.dev
BRAINTRUST_ORG_NAME="your-org-name"
BRAINTRUST_PROJECT_NAME=learn-bt-<your-name>
```

`BRAINTRUST_API_KEY` authenticates both the SDK and the CLI. The SDK uses it to
write traces, datasets, and evals. `BRAINTRUST_ORG_NAME` selects the target
organization for Gateway calls and must exactly match the org that owns your
API key. Keep `.env` private. Do not put a real key in `example.env` or commit
`.env`.

If your shell already exports `BRAINTRUST_API_KEY`, it takes precedence over
the value in `.env`. Remove that global export or run
`unset BRAINTRUST_API_KEY` before using this workshop, so the key in `.env`
selects the intended org.

## Step 3: Confirm that the CLI can reach your org

Install the `bt` CLI if it is not already available. The
[CLI quickstart](https://docs.braintrust.dev/reference/cli/quickstart)
has the installation command for your platform.

Then run this from the repository root:

```bash
bt projects list --env-file .env
```

You should see the projects in your Braintrust org. This confirms that the key
in `.env` works. `bt setup` is not needed for this workshop because it manages
separate CLI profiles and does not fill in the Python app's `.env` file.


## Check your setup

Confirm you have:

- A local `.venv` created by `uv sync`.
- A private `.env` with a valid API key, org name, and `BRAINTRUST_PROJECT_NAME`.
- A `learn-bt` project in your Braintrust org.

If `bt projects list` returns an authentication error, create a new API key in
Braintrust, replace the value in `.env`, and run the command again.
