# **Mock test**


## Dry run (to running immedietly)
make dry_run

## To startup
make venv-init
make init-env
make init-db
make migrate-up
make run


## To test
make venv-init (if not initialized)
make init-env (if not initialized)
make test


PORT in env.template is set too 3420