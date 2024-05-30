import requests
from lxml import etree
import re

def post_data(page):
    url = 'https://icsd-fiz-karlsruhe-de.proxy.library.cornell.edu/display/list.xhtml'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Cookie': 'ezproxy=KGhjsXjGUbSyI4h; ezproxyl=KGhjsXjGUbSyI4h; ezproxyn=KGhjsXjGUbSyI4h; ICSDCHECK=1716181636656; JSESSIONID=C6E27FA52B2ED6E00C1A2FDA239E42AC; FIZ-Cookie=238830221.16671.0000; _pk_ref.4.f192=%5B%22%22%2C%22%22%2C1716181637%2C%22https%3A%2F%2Fshibidp.cit.cornell.edu%2F%22%5D; _pk_id.4.f192=51380bec49db0515.1716181637.; _pk_ses.4.f192=1; mtm_consent_removed=; piwikNoticeClosed=true',
    }

    data = {
        'jakarta.faces.partial.ajax': True,
        'jakarta.faces.source': 'display_form:listViewTable',
        'jakarta.faces.partial.execute': 'display_form:listViewTable',
        'jakarta.faces.partial.render':' display_form:listViewTable display_form:selectedRowsLabel',
        'jakarta.faces.behavior.event': 'page',
        'jakarta.faces.partial.event': 'page',
        'display_form:listViewTable_pagination': True,
        'display_form:listViewTable_first': page * 10,
        'display_form:listViewTable_rows': 10,
        'display_form:listViewTable_skipChildren': True,
        'display_form:listViewTable_encodeFeature': True,
        'display_form': 'display_form',
        'display_form:j_idt46:shareLinkBackUrl': '#',
        'display_form:listViewTable_rppDD': 10,
        'display_form:listViewTable_selection': None,
        'display_form:listViewTable_columnOrder': 'display_form:listViewTable:j_idt71,display_form:listViewTable:listViewTableCollCodeColumn,display_form:listViewTable:listViewTableCcdcNoColumn,display_form:listViewTable:j_idt74,display_form:listViewTable:j_idt82,display_form:listViewTable:j_idt90,display_form:listViewTable:j_idt96,display_form:listViewTable:j_idt113,display_form:listViewTable:j_idt121,display_form:listViewTable:j_idt127,display_form:listViewTable:j_idt139,display_form:listViewTable:j_idt175,display_form:listViewTable:j_idt187,display_form:listViewTable:j_idt193,display_form:listViewTable:j_idt199,display_form:listViewTable:j_idt271,display_form:listViewTable:j_idt277,display_form:listViewTable:j_idt283,display_form:listViewTable:j_idt289,display_form:listViewTable:j_idt295,display_form:listViewTable:j_idt301,display_form:listViewTable:listViewTableQualityTagColumn,display_form:listViewTable:downloadColumn',
        'display_form:listViewTable_resizableColumnState': None,
        'display_form:expName': 'YourCustomFileName',
        'display_form:expCelltype:input_input': 'experimental',
        'jakarta.faces.ViewState': '7445271750243583794:-1527352541547582065',
    }

    response = requests.post(url, headers=headers, data=data)
    return response

def parse_data(response):

    html = response.text.replace('\r', '').replace('\n', '').replace('\r\n', '')
    # print(html)

    p = re.compile(r'id="display_form:listViewTable"\>\<\!\[CDATA\[(.*?)\<\/td\>\<\/tr\>\]\]')
    result = re.findall(p, html)
    # print(result)
    html = result[0] + '</td></tr>'
    # print(html)

    tree = etree.HTML(html)
    # print(tree)

    trs = tree.xpath('//tr')
    for tr in trs:
        code = tr.xpath('./td[2]/a/text()')[0]
        ccdc = tr.xpath('./td[3]/a/text()')
        if ccdc:
            ccdc = ccdc[0]
        else:
            ccdc = ''
        hms = tr.xpath('./td[4]/div/a/text()')
        if hms:
            hms = hms[0]
        else:
            hms = ''

        stuct = tr.xpath('./td[5]/div/a/text()')
        if stuct:
            stuct = stuct[0]
        else:
            stuct = ''

        stuct2 = tr.xpath('./td[6]/div/a/text()')
        if stuct2:
            stuct2 = stuct2[0]
        else:
            stuct2 = ''

        title = tr.xpath('./td[7]/div/a/text()')
        if title:
            title = title[0]
        else:
            title = ''

        authors = tr.xpath('./td[8]/div/a/text()')
        if authors:
            authors = authors[0]
        else:
            authors = ''

        referer = tr.xpath('./td[9]/a/div/text()')
        if referer:
            referer = referer[0]
        else:
            referer = ''

        cell = tr.xpath('./td[10]/a/div/text()')
        if cell:
            cell = cell[0]
        else:
            cell = ''

        stand = tr.xpath('./td[11]/a/div/text()')
        if stand:
            stand = stand[0]
        else:
            stand = ''

        value = tr.xpath('./td[12]/a/div/text()')
        if value:
            value = value[0]
        else:
            value = ''

        anx = tr.xpath('./td[13]/div/a/text()')
        if anx:
            anx = anx[0]
        else:
            anx = ''

        ab = tr.xpath('./td[14]/div/a/text()')
        if ab:
            ab = ab[0]
        else:
            ab = ''

        chemic = tr.xpath('./td[15]/div/a/text()')
        if chemic:
            chemic = chemic[0]
        else:
            chemic = ''

        pearso = tr.xpath('./td[16]/div/a/text()')
        if pearso:
            pearso = pearso[0]
        else:
            pearso = ''

        wyckof = tr.xpath('./td[17]/div/a/text()')
        if wyckof:
            wyckof = wyckof[0]
        else:
            wyckof = ''

        jour = tr.xpath('./td[18]/div/a/text()')
        if jour:
            jour = jour[0]
        else:
            jour = ''

        volume = tr.xpath('./td[19]/div/a/text()')
        if volume:
            volume = volume[0]
        else:
            volume = ''

        publica = tr.xpath('./td[20]/div/a/text()')
        if publica:
            publica = publica[0]
        else:
            publica = ''

        page = tr.xpath('./td[21]/a/div/text()')
        if page:
            page = page[0]
        else:
            page = ''


        print(code, ccdc, hms, stuct, stuct2, title, authors, referer, cell, stand, value, anx, ab, chemic, pearso, wyckof, volume,publica,page)


def run():
    for page in range(100):
        resource = post_data(page)
        parse_data(resource)


if __name__ == '__main__':
    run()
