from datetime import datetime
from tqdm import tqdm


def get_log(message, log_type='INFO'):
    """
    Module to return log message.

    :param message:  message want to show.
    :param log_type: type of log like INFO, ERROR, DEBUG, WARNING, ...
    :return: log message with log type, time and message.
    """
    time = (datetime.now()).strftime("%d-%m-%Y %H:%M:%S")
    log_mess = '[' + log_type.upper() + "] " + time + ' - ' + message.upper()
    return log_mess


def save_path(path: list, file_name=None, mode='stdout'):
    """
    Module writing path to screen or to file.

    :param path: path of searching result from BFS or DFS or other with the same structure.
    :param file_name: name of file to save result with `mode='write_to_file'`.
    :param mode: mode to write result to file (`mode='write_to_file'`) or to screen `mode='stdout'`.
    :return: Notification if save to file or warning empty if not exist path.
    """
    result = ['Beginning at vertex id: ' + str(path[0])]
    if not path:
        message = 'path is empty'
        print(get_log(message, log_type='WARNING'))
        return
    for vertex_id in path:  # collecting path data from `path`
        line = str(vertex_id)
        result.append(line)
    if mode.lower() == 'stdout':  # redirecting result to stdout of system
        print(get_log('Viewing mode: ' + mode.upper()))
        for line in result:
            print(get_log(line))
    elif mode.lower() == 'write_to_file':  # write result to file
        if not file_name:
            message = get_log('name of file is empty!', log_type='ERROR')
            raise ValueError(message)
        print(get_log('Viewing mode: ' + mode.upper()))
        print(get_log('WRITING RESULT TO FILE: ' + file_name))
        write_data = [result[0]] + ['\n--> ' + line for line in result[1:] + ['END']]
        with open(file_name, 'w') as f:
            for idx, line in zip(tqdm(range(len(write_data)), desc="Saving progress"), write_data):
                f.write(line)
            f.close()
        print(get_log('FINISHED SAVING DATA'))
