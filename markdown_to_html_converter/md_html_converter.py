# A Markdown to HTML converter
# Designed specifically for my workflow using Obsidian.md and upload to my Django application


from search_and_replace import *


folder_path = "C:\\input\\documents\\folder\\path\\goes\\here"
folder_out_path = "D:\\output\\path\\goes\\here"
document_name = "Essential Mathematics for CAD Designers.md"


# manually set the documents you want to include here
documents = [
    "System Basics\\Rhino UI Basics.md",
    "Essential Mathematics for CAD Designers.md",
    "System Basics\\Introduction to Rhino.md",
    "System Basics\\The Non-Uniform-Rational-Basis-Spline.md",
    "System Basics\\Modeling in Rhino.md",
    "Preface.md"
]


def convert_file(in_path, out_path):
    # open file
    in_file = open(in_path, "r")
    out_file = open(out_path, "w")
    raw_file_contents = in_file.read()

    # convert tags in a particular order
    headings_converted = convert_headings(raw_file_contents)
    print(len(headings_converted))
    hr_converted = convert_hr(headings_converted)
    print(len(hr_converted))
    img_converted = convert_img(hr_converted)
    print(len(img_converted))
    internal_links_converted = convert_internal_links(img_converted)
    print(len(internal_links_converted))
    external_links_converted = convert_external_links(internal_links_converted)
    print(len(external_links_converted))
    bulleted_list_converted = convert_bulleted_list(external_links_converted)
    print(len(bulleted_list_converted))
    enumerated_list_converted = convert_enumerated_list(bulleted_list_converted)
    print(len(enumerated_list_converted))
    bold_converted = convert_bold_text(enumerated_list_converted)
    print(len(bold_converted))

    # get the indices of latex pairs so we can exclude them from the italics conversion
    block_latex_pairs = find_latex_blocks(bold_converted)
    inline_latex_pairs = find_inline_latex(bold_converted, block_latex_pairs)
    all_latex_pairs = block_latex_pairs + inline_latex_pairs
    italics_converted = convert_italic_text(bold_converted, all_latex_pairs)
    print(len(italics_converted))

    avoid_regions = find_break_avoid_regions(italics_converted)
    breaks_converted = convert_breaks(italics_converted, avoid_regions)
    paragraph_avoid_regions = find_paragraph_avoid_regions(breaks_converted)

    paragraphs_converted = convert_paragraphs(breaks_converted, paragraph_avoid_regions)
    print(len(paragraphs_converted))

    out_file.write(paragraphs_converted)
    out_file.close()

for document in documents:
    print("Converting : " + document)
    file_in = folder_path + document
    file_out = folder_out_path + document[0:len(document) - 2 ] + "html"
    convert_file(file_in, file_out)
