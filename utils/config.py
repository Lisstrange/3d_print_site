from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.toml'],
    load_dotenv=True,
    environments=True,
    env_switcher="SERVICE_ENV",
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
