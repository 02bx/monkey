HIDDEN_FILE = '/var/tmp/.monkey-hidden-file'
HIDDEN_FOLDER = '/var/tmp/.monkey-hidden-folder'


def get_linux_commands_to_hide_files():
    return [
        'touch',    # create file
        HIDDEN_FILE,
        '; echo \"Successfully created hidden file: {}\" |'.format(HIDDEN_FILE),  # output
        'tee -a',   # and write to file
        HIDDEN_FILE
    ]


def get_linux_commands_to_hide_folders():
    return [
        'mkdir',    # make directory
        HIDDEN_FOLDER,
        '; touch',  # create file
        '{}/{}'.format(HIDDEN_FOLDER, 'some-file'),    # random file in hidden folder
        '; echo \"Successfully created hidden folder: {}\" |'.format(HIDDEN_FOLDER),  # output
        'tee -a',   # and write to file
        '{}/{}'.format(HIDDEN_FOLDER, 'some-file')     # random file in hidden folder
    ]


def get_linux_commands_to_delete():
    return [
        'rm',       # remove
        '-r',       # delete recursively
        '-f',       # force delete
        HIDDEN_FILE,
        HIDDEN_FOLDER
    ]
