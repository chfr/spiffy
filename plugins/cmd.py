def cmd(self, input):
    """Admin-only command, runs the supplied argument as Python code within the bot itself."""

    if input.isowner():
        cmd = input.args
        if not cmd:
            raise self.BadInputError()
        try:
            msg = u"\x02Result: \x02%s" % eval(cmd)
        except Exception, e:
            msg = "\x02Exception raised: \x02" + str(e)

        self.say(msg)

cmd.rule = ["cmd"]
cmd.usage = [("Run <command> and display the result","$pcmd <command>")]
cmd.example = [("Send a raw line of text to the IRC server","$pcmd self.sendLine('<data to send>')")]

