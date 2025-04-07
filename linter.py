#
# linter.py
# Linter for SublimeLinter4, a code checking framework for Sublime Text 3
#
# Written by Markus Liljedahl
# Copyright (c) 2017 Markus Liljedahl
#
# License: MIT
#

"""This module exports the AnsibleLint plugin class."""

from SublimeLinter.lint import Linter, util


class AnsibleLint(Linter):
    """Provides an interface to ansible-lint."""

    # linter settings
    cmd = ('ansible-lint', '${args}', '${file}')
    regex = r'^(?P<filename>^.+((\.yml)|(\.yaml))):(?P<line>\d+):(?P<col>\d*):? (?P<error>.+): (?P<message>.+)$'
    # -p generate non-multi-line, pep8 compatible output
    multiline = False

    # ansible-lint does not support column number
    #word_re = False
    #line_col_base = (1, 1)

    tempfile_suffix = 'yml'
    error_stream = util.STREAM_STDOUT

    defaults = {
        'selector': 'source.ansible',
        'args': '--nocolor -p',
        '--exclude= +': ['.galaxy'],
        '-c': '',
        '-r': '',
        '-R': '',
        '-t': '',
        '-x': '',
    }

    def __init__(self, view, settings):
        """If it uses Ansible Lint 5 will be updated the regex."""
        super(AnsibleLint, self).__init__(view, settings)

        # Must be resolved the path of Ansible Lint and Ansible if you'd like to use Ansible Lint 5.
        # Because the ansible will be called from Ansible Lint 5 in parsing playbook codes.
        # If the path doesn't resolve, an error for Ansible occurs when Ansible Lint execution.
        env = os.environ.copy()
        env_setting = self.settings.get('env', {})
        if env_setting and 'PATH' in env_setting.keys():
            env['PATH'] = env['PATH'] + ':%s' % env_setting['PATH']
