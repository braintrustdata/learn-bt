# 0.1 Set up the Braintrust CLI [CLI]

## Task

1. Install the `bt` CLI. See the
   [CLI quickstart](https://www.braintrust.dev/docs/reference/cli/quickstart) for
   the install command for your platform.
2. Run setup:
   First, `bt setup` will run through initializing the CLI. Authenticate with your Braintrust org and create a project for this course. It will also optionally ask to setup agent skills. It's highly recommended to set these up to allow coding agents to use Braintrust better.
   ```bash
   bt setup -i
   ```

3. Explore a couple of commands, for example:

   ```bash
   bt status
   bt projects list
   ```

4. Ask a coding agent to use the CLI to fetch the latest logs from a Braintrust
   project.


## Troubleshooting
- If install isn't successful, ensure there aren't any network or VPN blockers preventing the install.
- If `bt` command is unrecognized after install, ensure that it was added to your $PATH. This will vary by environment. Follow the instructions in the CLI after running install.
- If authentication is not working, ensure you are provisioned access to Braintrust for your organization.