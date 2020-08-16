from bs4 import BeautifulSoup

from BannerClass import BannerClass


class Parser:
    Classes = []

    readingClass = False

    def CurrentClass(self):
        return self.Classes[len(self.Classes) - 1]

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        for tag in soup.find_all('input', attrs={"name": True, "value": True}):
            name = tag['name']
            value = tag['value']

            # Reached end of classes
            if name == 'regs_row':
                # Includes dummy class
                if int(value) + 1 != len(self.Classes):
                    raise Exception('Error reading classes')

                break

            # Start reading class if not empty
            if name == 'assoc_term_in':
                self.readingClass = value != ''

                if self.readingClass:
                    self.Classes.append(BannerClass())

            if self.readingClass:
                self.CurrentClass().data[name] = value
