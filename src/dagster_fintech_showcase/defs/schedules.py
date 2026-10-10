import dagster as dg

fx_rates_job = dg.define_asset_job("fx_rates_job", selection=["fx_rates"])

fx_rates_schedule = dg.ScheduleDefinition(
    job=fx_rates_job,
    cron_schedule="0 * * * *",
    execution_timezone="Asia/Kolkata",
    default_status=dg.DefaultScheduleStatus.RUNNING,
)