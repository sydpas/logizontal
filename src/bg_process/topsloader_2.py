from bg_process.logloader_1 import (logsection)


def top_load(file_path):
    """
    This function reads an LAS file and creates a list of all the well tops.

    Return:
        well_tops_list: list of all well tops from an LAS file.
    """
    tops_begin = False
    tops = {}

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            if line.startswith('~TOPS_Data'):
                tops_begin = True
                continue  # to skip the header line

            if tops_begin:
                if line == '' or line.startswith('~'):
                    break  # to end the tops section

                sec = line.split()
                if len(sec) >= 2:  # to join name sections
                    try:
                        depth = float(sec[-1])
                        name = ' '.join(sec[:-1])
                        tops[name] = depth
                    except ValueError:
                        continue

    # convert to ss using kb
    _, _, _, _, _, _, kb = logsection(file_path)
    tops_subsea = {name: kb - depth for name, depth in tops.items()}
    print(f'subsea tops: {tops_subsea}')

    return [tops_subsea]



