def test_htmldocx(article_div):
    # pip htmldocx
    from htmldocx import HtmlToDocx

    new_parser = HtmlToDocx()
    new_parser.parse_html_string(article_div)
    new_parser.doc.save('htmldoc.docx')

test_htmldocx(article_div)