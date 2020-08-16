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

            if name == 'assoc_term_in':
                self.Classes.append(BannerClass())
                self.readingClass = True

            if self.readingClass:
                self.CurrentClass().data[name] = tag['value']

                # Reached end of class
                if name == 'MESG':
                    self.readingClass = False