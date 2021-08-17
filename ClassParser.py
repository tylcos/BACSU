from bs4 import BeautifulSoup

from BannerClass import BannerClass


class ClassParser:
    Classes = []

    readingClass = False

    def CurrentClass(self):
        return self.Classes[-1]

    def __init__(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        for tag in soup.find_all('input', attrs={"name": True, "value": True}):
            name = tag['name']
            value = tag['value']

            # Reached end of classes
            if name == 'regs_row':
                if int(value) != len(self.Classes):
                    raise Exception(f'Error reading classes, read {len(self.Classes)} classes')

                break

            # Start reading class if not empty
            if name == 'assoc_term_in' and value != 'DUMMY':
                self.readingClass = value != ''

                if self.readingClass:
                    self.Classes.append(BannerClass())

            if self.readingClass and name != 'RSTS_IN':
                self.CurrentClass().data[name] = value
