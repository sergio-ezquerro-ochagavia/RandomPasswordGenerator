import argparse
from genericpath import isdir
import secrets
import logging
import os
from pathlib import Path
import string


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    # param declaration
    pw_times: int
    pw_len: int
    file_path: Path

    upper: bool
    lower: bool
    numerical: bool
    symbol: bool
    to_print: bool
    to_save: bool
    override_file: bool

    # args
    if args.times:
        pw_times = args.times
    if args.length:
        pw_len = args.length
    if args.file:
        file_path = Path(args.file)

    upper = args.u
    lower = args.l
    numerical = args.n
    symbol = args.x
    to_print = args.p
    to_save = args.s
    override_file = args.o

    # param adjustments
    if not (upper or lower or numerical or symbol):
        upper = True
        lower = True
        numerical = True
        symbol = True

    no_out: bool = not (to_print or to_save)
    is_w_gui: bool = os.name == "nt" and "PROMPT" not in os.environ

    if no_out:
        if is_w_gui:
            to_save = True
        else:
            to_print = True

    # logic
    result: str = gen_pw(pw_times, pw_len, upper, lower, numerical, symbol)

    if to_print:
        print(result)

    if to_save:
        save_file(override_file, file_path, result)

    if is_w_gui:
        os.system("pause")


def save_file(override_file: bool, file_path: Path, result: str):
    if not isdir(file_path):
        # write to file
        if override_file:
            with open(file_path, "w") as f:
                f.write(result)
        # append to file
        else:
            with open(file_path, "a") as f:
                if os.path.getsize(file_path) != 0:
                    f.write("\n")
                f.write(result)

        logging.debug("Password(s) written to file")
    else:
        logging.error("path is a directory")


def get_samples(upper: bool, lower: bool, num: bool, symb: bool):
    samples: str = ""
    if upper:
        samples += string.ascii_uppercase
    if lower:
        samples += string.ascii_lowercase
    if num:
        samples += string.digits
    if symb:
        samples += string.punctuation
    return samples


def gen_pw(times: int, lenght: int, upper: bool, lower: bool, num: bool, symb: bool):
    pws = []

    charset = get_samples(upper, lower, num, symb)
    for _ in range(times):
        pw : str = ''.join(secrets.choice(charset) for _ in range(lenght))
        pws.append(pw)
    result = pws.join('\n')
    
    return result

def get_parser():
    epilog_array = []
    epilog_array.append('Valid examples:')
    epilog_array.append('')
    epilog_array.append('> Generate 5 passwords with 20 characters each, using uppercase, lowercase and number characters, and print them as output')
    epilog_array.append('    py RandPwGen.py -times 5 -length 20 -puln')
    epilog_array.append('> Generate 10 passwords with 16 characters each, using uppercase, lowercase, number and symbol characters, and save them to the default file "pwds.txt"')
    epilog_array.append('    py RandPwGen.py -times 10 -length 16 -s')
    epilog_array.append('> Generate 1 password with 16 characters, and save it to "passwords.txt", overriding whatever was in it in the case it existed before')
    epilog_array.append('    py RandPwGen.py -file "passwords.txt" -so')
    epilog_array.append('')
    epilog_array.append('')
    epilog_array.append("As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like \"%(prog)s '@params.conf'\".")
    epilog_array.append("    Example: py RandPwGen.py '@params.conf'")
    
    
    epilog_str = ''
    for line in epilog_array:
        epilog_str += line + "\n"
    
    
    parser = argparse.ArgumentParser(
        description="The script in this project generates passwords. You can run the python script file either from the command line or graphically.",
        epilog=epilog_str,
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # Parameter group declaration
    group_ch = parser.add_argument_group(title="included characters", description=None)
    group_out = parser.add_argument_group(title="output", description=None)

    # Parameters here.
    parser.add_argument(
        "-times", type=int, default=1, help="number of passwords to generate"
    )
    parser.add_argument(
        "-length", type=int, default=20, help="length of passwords to generate"
    )

    # included characters group
    group_ch.add_argument(
        "-u", help="include uppercase characters", action="store_true"
    )
    group_ch.add_argument(
        "-l", help="include lowercase characters", action="store_true"
    )
    group_ch.add_argument("-n", help="include numbers", action="store_true")
    group_ch.add_argument("-x", help="include symbols", action="store_true")

    # output group
    group_out.add_argument(
        "-p", help="print the generated passwords", action="store_true"
    )
    group_out.add_argument(
        "-s", help="save generated passwords in file", action="store_true"
    )
    group_out.add_argument("-o", help="overwrite file", action="store_true")
    group_out.add_argument("-file", default="pwds.txt", help="path of file to generate")
    group_out.add_argument(
        "-v", "--verbose", help="deeper logging information", action="store_true"
    )
    
    return parser

if __name__ == "__main__":
    
    parser = get_parser()

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    # print(args);

    main(args, loglevel)
