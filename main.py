# Introduction
# LogScroll is an interpretive log reader that takes a log and allows a user to
# scroll forwards and backwards through the log. This is accomplished by
# defining a set of Patterns that check if a line matches, then perform some
# transformation of the state.

# There are three components to the state:
# * Objects
# * Stack Trace
# * Command Stack

# LogScroll works by defining a set of commands, then translating lines of a log into commands.
# We use a plugin architecture


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
