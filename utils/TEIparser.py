from bs4 import BeautifulSoup

from dataclasses import dataclass





#print(soup.title.getText())
#print(soup.abstract.getText(separator=' ', strip=True))

#print(soup.find('idno', type='DOI'))
#print('ole')


class TEIFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.soup = read_tei(filename)
        self._text = None
        self._title = ''
        self._abstract = ''

    @property
    def doi(self):
        idno_elem = self.soup.find('idno', type='DOI')
        if not idno_elem:
            return ''
        else:
            return idno_elem.getText()

    @property
    def title(self):
        if not self._title:
            self._title = self.soup.title.getText()
        return self._title

    @property
    def abstract(self):
        if not self._abstract:
            abstract = self.soup.abstract.getText(separator=' ', strip=True)
            self._abstract = abstract
        return self._abstract

    @property
    def authors(self):
        authors_in_header = self.soup.analytic.find_all('author')
        result = []
        for author in authors_in_header:
            persname = author.persName
            if not persname:
                continue
            firstname = elem_to_text(persname.find("forename", type="first"))
            middlename = elem_to_text(persname.find("forename", type="middle"))
            surname = elem_to_text(persname.surname)
            person = Person(firstname, middlename, surname)
            result.append(person)
        return result
    
    @property
    def text(self):
        sections = []
        figures = {}
        tables = {}
        if not self._text:
            ## Extract Tables
            for table in self.soup.body.find_all("figure", type="table"):
                tableHead = table.head.extract()
                tableText = table.get_text(separator=' ', strip=True)
                tables[tableHead] = tableText
                table.extract()
            ## Extract Figures
            for figure in self.soup.body.find_all("figure"):
                    figureHead = figure.head
                    figureHead.extract()
                    figureText = figure.get_text(separator=' ', strip=True)
                    figures[figureHead.get_text] = figureText
                    figure.extract()
            
            for div in self.soup.body.find_all("div"):
                # div is neither an appendix nor references, just plain text.
                if not div.get("type"):
                    if div.head:
                        head = div.head.extract().get_text()
                        paragraphsStrigs = []
                        for paragraph in div.find_all("p"):
                            paragraphsStrigs.append(paragraph.get_text(separator=' ', strip=True))
                        sections.append({"section_name": head, "paragraphs": paragraphsStrigs})
                    else:
                        paragraphsStrigs = []
                        for paragraph in div.find_all("p"):
                            paragraphsStrigs.append(paragraph.get_text(separator=' ', strip=True))
                        sections.append({"section_name":"noSectionName", "paragraphs":paragraphsStrigs})

        return {"sections":sections, "figures":figures, "tables": tables}

def elem_to_text(elem, default=''):
    if elem:
        return elem.getText()
    else:
        return default

def read_tei(filename):
    tei_doc = filename
    with open(tei_doc, 'rb') as tei:
        soup = BeautifulSoup(tei, 'xml')
    return soup

@dataclass
class Person:
    firstname: str
    middlename: str
    surname: str


