# 0.1 Set up the local environment [CLI]

Before you instrument the app, give the Python SDK and the Braintrust CLI the
credentials they need. The API key determines which Braintrust org receives
your traces. The project is selected later in code.

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

Open `.env` and replace the placeholders. Quote an org name that contains a
space.

```dotenv
BRAINTRUST_API_KEY=your-api-key
BRAINTRUST_ORG_NAME="your-org-name"
BASE_URL=https://gateway.braintrust.dev
```

`BRAINTRUST_API_KEY` authenticates both the SDK and the CLI. The SDK uses it to
write traces, datasets, and evals. `BRAINTRUST_ORG_NAME` is sent to the
Braintrust Gateway when the app makes a model call. Keep `.env` private. Do
not put a real key in `example.env` or commit `.env`.

## Step 3: Confirm that the CLI can reach your org

Install the `bt` CLI if it is not already available. The
[CLI quickstart](https://www.braintrust.dev/docs/reference/cli/quickstart)
has the installation command for your platform.

Then run this from the repository root:

```bash
bt projects list --env-file .env
```

You should see the projects in your Braintrust org. This confirms that the key
in `.env` works. `bt setup` is not needed for this workshop because it manages
separate CLI profiles and does not fill in the Python app's `.env` file.

## Step 4: Create the course project

Create a dedicated project for the workshop:

```bash
bt projects create learn-bt --env-file .env
```

If the project already exists, keep using it. In Exercise 1.1,
`braintrust.init_logger(project="learn-bt")` sends the app's traces to this
project.

## Check your setup

At this point, you should have all of the following:

- A local `.venv` created by `uv sync`.
- A private `.env` with a valid API key and org name.
- A `learn-bt` project in your Braintrust org.

If `bt projects list` returns an authentication error, create a new API key in
Braintrust, replace the value in `.env`, and run the command again.
