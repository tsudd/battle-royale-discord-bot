async def info(ctx):
    logging.info(f"Passed help command with context - {ctx}")
    ans = "Existing commands:\n"
    for st in COMMANDS:
        ans += st + '\n'
    await ctx.channel.send(ans)
