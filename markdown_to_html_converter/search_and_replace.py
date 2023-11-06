
# for directing internal links
site_path = "http://path/to/site/goes/here/"

# Searches for headings in the document and converts them to tags
def convert_headings(data_in):
    
    # first, we find the indices of the header tags
    index = 0
    index_list = []

    while index != -1:
        cur_index = data_in.find('#', index)
        if(cur_index == -1):
            index = cur_index
        else:
            index_list.append(cur_index)
            index = cur_index + 1

    # Now we want to identify which ones are grouped together to define our different levels of headers
    # we will make a new list that has the form [starting_index, tag number (1-6)]
    sorted_indices = []

    i = 0
    for _ in range(len(index_list)):
        tag_counter = 1
        same_tag = True
        while same_tag and i < len(index_list):
            if (i < len(index_list) - 1) and ((int(index_list[i + 1]) - int(index_list[i])) == 1):
                tag_counter = tag_counter + 1
            else:
                same_tag = False
                sorted_indices.append([index_list[i - tag_counter + 1], tag_counter])
            i = i + 1

    # Use our list of indices to modify our original data
    sorted_indices.reverse()
    for tag in sorted_indices:
        temp_index = tag[0]
        temp_head_val = tag[1]
        # Extract the header text
        newline_index = data_in.find('\n', temp_index)
        heading_text = data_in[temp_index + temp_head_val + 1 : newline_index]
        heading_text_no_spaces = heading_text.replace(" ", "_")
        htext = "h" + str(temp_head_val)
        open_tag = "<" + htext + " id=\"" + heading_text_no_spaces + "\">"
        close_tag = "</" + htext + ">"
        new_line = open_tag + heading_text + close_tag
        data_in = data_in[0:temp_index] + new_line + data_in[newline_index : len(data_in)]

    data_out = data_in
    return data_out

# Replaces Horizontal Rules
def convert_hr(data_in):

    index = 0
    index_list = []

    # find the horizontal rules
    while index != -1:
        cur_index = data_in.find('---', index)
        if(cur_index == -1):
            index = cur_index
        else:
            index_list.append(cur_index)
            index = cur_index + 2
    
    # replace the rules with the proper HTML tag
    index_list.reverse()
    for rule_index in index_list:
        hr_tag_string = "<hr>"
        data_in = data_in[0:rule_index] + hr_tag_string + data_in[rule_index + 3 : len(data_in)]

    data_out = data_in
    return data_out

# Converts image references
def convert_img(data_in):
    
    index = 0
    index_start_list = []
    index_link_start_list = []
    index_end_list = []

    # find all the starting indices
    while index != -1:
        cur_index = data_in.find('![', index)
        if(cur_index == -1):
            index = cur_index
        else:
            index_start_list.append(cur_index)
            index = cur_index + 2


    # find all the ending indices
    for x in index_start_list:
        link_start_index = data_in.find('(', x)
        end_index = data_in.find(')', x)
        index_link_start_list.append(link_start_index)
        index_end_list.append(end_index)

    # build strings and replace occurances
    index_start_list.reverse()
    index_link_start_list.reverse()
    index_end_list.reverse()
    for x in range(len(index_link_start_list)):
        alt_text = data_in[index_start_list[x] + 2 : index_link_start_list[x] - 1]
        link_text = data_in[index_link_start_list[x] + 1 : index_end_list[x]]
        tag_1 = "<img src=\""
        tag_2 = "\" alt=\""
        tag_3 = "\">"
        constructed_tag = tag_1 + link_text + tag_2 + alt_text + tag_3
        data_in = data_in[0 : index_start_list[x]] + constructed_tag + data_in[index_end_list[x] + 1 : len(data_in)]


    data_out = data_in
    return data_out

# Replaces hyperlink references
def convert_external_links(data_in):

    index = 0
    index_start_list = []
    index_text_end_list = []
    index_link_start_list = []
    index_end_list = []

    text_start_token = "["
    text_end_token = "]"
    link_start_token = "("
    link_end_token = ")"

    # Find the start indices of external link occurances
    while index != -1:
        cur_index = data_in.find(text_start_token, index)
        if(cur_index == -1):
            index = cur_index
        else:
            index_start_list.append(cur_index)
            index = cur_index + 1

    remove_list = []
    # find the remaining useful indices for our link tokens
    for x in index_start_list:
        text_end_index = data_in.find(text_end_token, x)
        link_start_index = data_in.find(link_start_token, x)
        link_end_index = data_in.find(link_end_token, x)
        external_link = text_end_index + 1 == link_start_index
        
        if external_link:
            index_text_end_list.append(text_end_index)
            index_link_start_list.append(link_start_index)
            index_end_list.append(link_end_index)
        else:
            remove_list.append(x)
    
    # remove any that aren't links
    for x in remove_list:
        index_start_list.remove(x)

    # reverse the lists so our indexing isn't messed up by replacing text
    index_start_list.reverse()
    index_text_end_list.reverse()
    index_link_start_list.reverse()
    index_end_list.reverse()
    for x in range(len(index_start_list)):
        text = data_in[index_start_list[x] + 1 : index_text_end_list[x]]
        link = data_in[index_link_start_list[x] + 1 : index_end_list[x]]
        tag_start = "<a href=\"" + site_path
        tag_mid = "\">"
        tag_end = "</a>"
        constructed_tag = tag_start + link + tag_mid + text + tag_end
        # replace our markdown tag
        data_in = data_in[0:index_start_list[x]] + constructed_tag + data_in[index_end_list[x] + 1 : len(data_in)]


    data_out = data_in
    return data_out


# Replaces internal link references
def convert_internal_links(data_in):
    
    index = 0
    index_start_list = []
    index_end_list = []

    text_start_token = "[["
    text_end_token = "]]"

    # Find the start inices and load a list
    while index != -1:
        cur_index = data_in.find(text_start_token, index)
        if(cur_index == -1):
            index = cur_index
        else:
            index_start_list.append(cur_index)
            index = cur_index + 1

    # find the end indices and load a parallel list
    for x in index_start_list:
        end_index = data_in.find(text_end_token, x)
        index_end_list.append(end_index)
    
    index_start_list.reverse()
    index_end_list.reverse()

    # extract and reform the data
    for x in range(len(index_start_list)):
        # Extract the section we want to link to
        linked_section_name = data_in[index_start_list[x] + 2 : index_end_list[x]]
        # construct the string we will be replacing our markdown with
        tag_start = "<a href=\"" + site_path
        tag_mid = "\">"
        tag_end = "</a>"
        constructed_tag = tag_start + linked_section_name + tag_mid + linked_section_name + tag_end
        # replace our markdown tag
        data_in = data_in[0:index_start_list[x]] + constructed_tag + data_in[index_end_list[x] + 2 : len(data_in)]

    data_out = data_in
    return data_out


def count_newline(data_in):
    index = 0 
    char = "\n"
    newline_list = []

    while index != -1:
        cur_index = data_in.find(char, index)
        if(cur_index == -1):
            index = cur_index
        else:
            newline_list.append(cur_index)
            index = cur_index + 1
    
    print(newline_list)
    print(len(newline_list))


# Converts bulleted lists
def convert_bulleted_list(data_in):
    index = 0
    delimeter = "\n- "
    bullet_list = []

    # find all the bullet points
    while index != -1:
        cur_index = data_in.find(delimeter, index)
        if(cur_index == -1):
            index = cur_index
        else:
            bullet_list.append(cur_index)
            index = cur_index + 2

    groups = []
    temp_group = []
    
    # group together bullet lists
    for x in bullet_list:
        next_newline = data_in.find("\n", x + 1)
        next_char = data_in[next_newline+1]
        if(next_char == "-"):
            temp_group.append(x)
        else:
            temp_group.append(x)
            groups.append(temp_group.copy())
            temp_group.clear()

    groups.reverse()
    
    for group in groups:
        # Construct an unordered list
        compiled_string = ""
        open_ul_tag = "\n<ul>\n"
        close_ul_tag = "</ul>"
        open_li_tag = "<li>"
        close_li_tag = "</li>\n"
        compiled_string = compiled_string + open_ul_tag
        
        for bullet in group:
            #extract information, construct bullet, append to list
            bullet_index = bullet + 1
            next_newline = data_in.find("\n", bullet_index)
            list_item = data_in[bullet_index + 2 : next_newline]
            list_item_string = open_li_tag + list_item + close_li_tag
            compiled_string = compiled_string + list_item_string
        
        # close out our string string and replace our 
        compiled_string = compiled_string + close_ul_tag
        end_of_group = data_in.find("\n", group[-1] + 1)
        data_in = data_in[0:group[0]+1] + compiled_string + data_in[end_of_group : len(data_in)]


    data_out = data_in
    return data_out


# Converts enumerated lists
def convert_enumerated_list(data_in):
    index = 0
    delimeter = "\n1. "
    list_start_positions = []

    while index != -1:
        cur_index = data_in.find(delimeter, index)
        if(cur_index == -1):
            index = cur_index
        else:
            list_start_positions.append(cur_index)
            index = cur_index + 2

    list_start_positions.reverse()

    for start_index in list_start_positions:
        # Variables to keep tracking of how long the list has been
        list_continuing = True
        current_list_value = 1
        cur_index = start_index + 1
        # initialize and construct the first line
        compiled_string = "\n<ol>\n"
        end_first_line = data_in.find("\n", cur_index)
        first_line = "<li>" + data_in[cur_index + 3 : end_first_line] + "</li>\n"
        compiled_string = compiled_string + first_line
        # start a loop that will run until the next expected number is not present
        while list_continuing:
            current_list_value += 1
            next_line = data_in.find("\n", cur_index)
            if(current_list_value < 10):
                temp_value = data_in[next_line + 1 : next_line + 2]
            else:
                temp_value = data_in[next_line + 1 : next_line + 3]
            expected_value = str(current_list_value)
            if(temp_value == expected_value):
                cur_index = next_line + 1
                end_line = data_in.find("\n", cur_index)
                item_text = "<li>" + data_in[cur_index + 3 : end_line] + "</li>\n"
                # print(item_text)
                compiled_string = compiled_string + item_text
            else:
                list_continuing = False
        # Complete the block and replace it in the file
        compiled_string = compiled_string + "</ol>"
        next_line = data_in.find("\n", cur_index + 1)
        data_in = data_in[0 : start_index + 1] + compiled_string + data_in[next_line : len(data_in)]


    data_out = data_in
    return data_out


# Converts bold words
def convert_bold_text(data_in):
    index = 0
    delimeter = "**"
    occurances = []
    
    # find all occurances
    while index != -1:
        cur_index = data_in.find(delimeter, index)
        if(cur_index == -1):
            index = cur_index
        else:
            occurances.append(cur_index)
            index = cur_index + 1
    #print(len(data_in))
    #print(len(occurances))
    occurances.reverse()
    
    # They should always come in pairs, search and replace the pairs
    for x in range(0, len(occurances), 2):
        start_index = occurances[x + 1]
        end_index = occurances[x]
        bold_text = data_in[start_index + 2 : end_index]
        bold_tags = "<b>" + bold_text + "</b>"
        data_in = data_in[0 : start_index] + bold_tags + data_in[end_index + 2 : len(data_in)]
    

    data_out = data_in
    return data_out

# returns a list of the indices of a substring(delimeter) in a string(data)
def find_occurances_of(delimeter, data):
    occurances = []
    index = 0

    while index != -1:
        cur_index = data.find(delimeter, index)
        if(cur_index == -1):
            index = cur_index
        else:
            occurances.append(cur_index)
            index = cur_index + len(delimeter)
    
    return occurances

def find_occurances_of_single_step(delimeter, data):
    occurances = []
    index = 0

    while index != -1:
        cur_index = data.find(delimeter, index)
        if(cur_index == -1):
            index = cur_index
        else:
            occurances.append(cur_index)
            index = cur_index + 1
    
    return occurances

def find_latex_blocks(data_in):
    occurances = find_occurances_of("$$", data_in)
    paired_values = []

    for x in range(0, len(occurances), 2):
        pair = [occurances[x], occurances[x+1]]
        paired_values.append(pair)

    return paired_values

def find_inline_latex(data_in, latex_block_list):
    occurances = find_occurances_of("$", data_in)
    remove_occurances = []
    for x in occurances:
        for block in latex_block_list:
            if(x >= block[0] and x <= block[1] + 1):
                remove_occurances.append(x)
    
    #remove any repeats
    remove_occurances = [*set(remove_occurances)]

    for repeat in remove_occurances:
        occurances.remove(repeat)
    
    paired_values = []
    for x in range(0, len(occurances), 2):
        pair = [occurances[x], occurances[x + 1]]
        paired_values.append(pair)
    
    return paired_values


# Converts italic words, ignore the avoid pairs
def convert_italic_text(data_in, avoid_pairs):
    index = 0
    delimeter = "*"
    occurances = []
    
    # find all occurances
    while index != -1:
        cur_index = data_in.find(delimeter, index)
        if(cur_index == -1):
            index = cur_index
        else:
            occurances.append(cur_index)
            index = cur_index + 2

    occurances_remove_list = []
    for x in occurances:
        for pair in avoid_pairs:
            if(x >= pair[0] and x <= pair[1]):
                occurances_remove_list.append(x)
    
    #remove any repeats
    occurances_remove_list = [*set(occurances_remove_list)]

    for avoid in occurances_remove_list:
        occurances.remove(avoid)
    print("occurances : " + str(len(occurances)))
    occurances.reverse()
    
    # They should always come in pairs, search and replace the pairs
    for x in range(0, len(occurances), 2):
        start_index = occurances[x + 1]
        end_index = occurances[x]
        italic_text = data_in[start_index + 1 : end_index]
        italic_tags = "<i>" + italic_text + "</i>"
        data_in = data_in[0 : start_index] + italic_tags + data_in[end_index + 1 : len(data_in)]
    

    data_out = data_in
    return data_out

# Converts text blocks to paragraphs and places line breaks in between

def find_break_avoid_regions(data_in):
    avoid_regions = []
    # find headings and add to list
    for x in range(1,7):
        start_tag = "<h" + str(x) + ">"
        end_tag = "</h" + str(x) + ">"
        start_tags = find_occurances_of(start_tag, data_in)
        end_tags = find_occurances_of(end_tag, data_in)
        if(len(start_tags) != 0):
            for y in range(len(start_tags)):
                avoid_regions.append([start_tags[y], end_tags[y] + len(end_tag) - 1])

    # find horizontal rules and add to list
    hr_tags = find_occurances_of("<hr>", data_in)
    for tag in hr_tags:
        avoid_regions.append([tag, tag + len("<hr>") - 1])

    # find images and add to list
    image_tags = find_occurances_of("<img", data_in)
    image_close_brackets = []

    for tag in image_tags:
        close_bracket = data_in.find(">", tag)
        image_close_brackets.append(close_bracket)

    for x in range(len(image_tags)):
        avoid_regions.append([image_tags[x], image_close_brackets[x]])

    # find links and add to list
    # link_start_tag = "<a href"
    # link_end_tag = "</a>"
    
    # link_starts = find_occurances_of(link_start_tag, data_in)
    # link_ends = find_occurances_of(link_end_tag, data_in)

    # for x in range(len(link_starts)):
    #     avoid_regions.append([link_starts[x], link_ends[x] + len(link_end_tag) - 1])

    # find uls and add to list
    ul_open_tag = "<ul>"
    ul_close_tag = "</ul>"
    ul_open_tags = find_occurances_of(ul_open_tag, data_in)
    ul_close_tags = find_occurances_of(ul_close_tag, data_in)

    for x in range(len(ul_open_tags)):
        avoid_regions.append([ul_open_tags[x], ul_close_tags[x] + len(ul_close_tag) - 1])
    
    # find ols and add to list
    ol_open_tag = "<ol>"
    ol_close_tag = "</ol>"
    ol_open_tags = find_occurances_of(ol_open_tag, data_in)
    ol_close_tags = find_occurances_of(ol_close_tag, data_in)

    for x in range(len(ol_open_tags)):
        avoid_regions.append([ol_open_tags[x], ol_close_tags[x] + len(ol_close_tag) - 1])


    # find latex blocks and add to list
    latex_blocks = find_latex_blocks(data_in)
    for block in latex_blocks:
        avoid_regions.append(block)

    return avoid_regions

def find_paragraph_avoid_regions(data_in):
    avoid_regions = []
    # find headings and add to list
    for x in range(1,7):
        start_tag = "<h" + str(x) + ">"
        end_tag = "</h" + str(x) + ">"
        start_tags = find_occurances_of(start_tag, data_in)
        end_tags = find_occurances_of(end_tag, data_in)
        if(len(start_tags) != 0):
            for y in range(len(start_tags)):
                avoid_regions.append([start_tags[y], end_tags[y] + len(end_tag) - 1])

    # find horizontal rules and add to list
    hr_tags = find_occurances_of("<hr>", data_in)
    for tag in hr_tags:
        avoid_regions.append([tag, tag + len("<hr>") - 1])

    # find images and add to list
    image_tags = find_occurances_of("<img", data_in)
    image_close_brackets = []

    for tag in image_tags:
        close_bracket = data_in.find(">", tag)
        image_close_brackets.append(close_bracket)

    for x in range(len(image_tags)):
        avoid_regions.append([image_tags[x], image_close_brackets[x]])

    # find uls and add to list
    ul_open_tag = "<ul>"
    ul_close_tag = "</ul>"
    ul_open_tags = find_occurances_of(ul_open_tag, data_in)
    ul_close_tags = find_occurances_of(ul_close_tag, data_in)

    for x in range(len(ul_open_tags)):
        avoid_regions.append([ul_open_tags[x]+1, ul_close_tags[x] + len(ul_close_tag) - 1])
    
    # find ols and add to list
    ol_open_tag = "<ol>"
    ol_close_tag = "</ol>"
    ol_open_tags = find_occurances_of(ol_open_tag, data_in)
    ol_close_tags = find_occurances_of(ol_close_tag, data_in)

    for x in range(len(ol_open_tags)):
        avoid_regions.append([ol_open_tags[x]+1, ol_close_tags[x] + len(ol_close_tag) - 1])


    # find latex blocks and add to list
    latex_blocks = find_latex_blocks(data_in)
    for block in latex_blocks:
        avoid_regions.append(block)

    # find double breaks
    breaks = find_occurances_of("<br>", data_in)
    #print(breaks)
    for x in range(len(breaks) - 1):
        if(breaks[x + 1] - breaks[x] <= 7):

            avoid_regions.append([breaks[x], breaks[x+1]])

    return avoid_regions

def convert_breaks(data_in, avoid_regions):
    double_newlines = find_occurances_of_single_step("\n\n", data_in)
    remove_list = []

    for br in double_newlines:
        for region in avoid_regions:
            if(br >= region[0] and br <= region[1]):
                remove_list.append(br)
    remove_list = [*set(remove_list)]
    print(remove_list)
    for items in remove_list:
        double_newlines.remove(items)
    
    double_newlines.reverse()

    for br in double_newlines:
        data_in = data_in[0 : br + 1] + "<br>" + data_in[br + 1 : len(data_in)]

    data_out = data_in
    return data_out

def convert_paragraphs(data_in, avoid_regions):
    breaks = find_occurances_of("<br>", data_in)
    paragraph_bools = []

    for x in range(0, len(breaks) - 1):
        for region in avoid_regions:
            if(region[0] >= breaks[x] and region[1] <= breaks[x+1]):
                paragraph_bools.append(x)
    
    paragraph_bools = [*set(paragraph_bools)]

    for x in range(len(breaks) - 2, 0, -1):
        if x not in paragraph_bools:
            data_in = data_in[0 : breaks[x] + len("<br>\n")] + "<p>\n" + data_in[breaks[x] + len("<br>\n") : breaks[x+1]] + "</p>\n" + data_in[breaks[x+1] : len(data_in)]

    data_out = data_in
    return data_out
