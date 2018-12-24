# Config File Handler
import fo 
##import ekhnet as s
from Printer import SpoolPrinter
import Printer as p
class cfh (object):
    def __init__(self, target):
        self.target = target

    def generate_conf(self, fl_name, comments, section_ls):

        # Validating
        # s.check_str(fl_name)
        # s.check_str(comments)
        # s.check_list(section_ls)

        # Making spool printer
        sp = SpoolPrinter(self.target, overwrite=True)

        # Making new file if one does not already exist
        if not fo.verify_file_exists(self.target):
            sp.overwrite_file()

        # Printing header
        sp.println(p.print_header(fl_name))

        # Generating comments, line by line
        comments_ls = comments.split(' ')
        y = 0
        line_str = ''
        words_per_line = 8
        for x in comments_ls:
            line_str += ' ' + str(x)
            y += 1
            if y > words_per_line:
                sp.println('#' + str(line_str))
                y = 0
                line_str = ''

        # Adding breathing room gap before section starts
        sp.println('')

        # Starting Sections
        for x in section_ls:
            sp.println('[' + str(x) + ']')
            sp.println(' ')
            sp.println(' ')
            sp.println(' ')

        # THE END IS NEAR
        sp.println('[end]')

        sp.println(p.print_footer('Sekhnet'))

    def read_conf(self):
        fo.check_path(self.target)

        conf_ls = []

        # Getting info from file
        with open(self.target) as conf:
            for line in conf:
                conf_ls.append(str(line))

        value_dic = {}
        current_var = None

        for x in range(len(conf_ls)):
            if conf_ls[x][0] == '#':
                continue


            if conf_ls[x][0] == '[':
                # Breaking when we reach the end
                if conf_ls[x] == '[end]':
                    break

                # Sets new list in dictionary for section
                current_var = conf_ls[x][1:-2]
                value_dic[current_var] = []
                continue

            # This will only trigger if we are currently recording a section
            if current_var is not None:
                line = conf_ls[x][:-1]
                if line == ' ':
                    continue
                value_dic[current_var].append(line)

        value_dic.pop('end')
        return value_dic

if __name__ == '__main__':
    test = cfh('dir_locations.conf')
    params = ['Fargus', 'Encrypted', 'directories']
    #test.generate_conf('Sekhnet ', 'these are a lot of words that I am typing which should be limited to 4 words per line but we will see what the final result is.', params)

    print(test.read_conf())








