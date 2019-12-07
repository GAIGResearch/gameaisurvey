from py.q_process import *

file_path = "../_data/Game AI Survey.csv"
cols_skip = 2  # The first 2 columns are timestamp and name, skip these

# multiple_choice = 0, free_text = 1, short_text = 2
q_types = [2, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # TODO: Should be one value per question

# Some plots get too large with full labels. This is a map from question title to character separating an abbreviation
# in the answers, e.g. "long text (abrev)" would use only the word in brackets, if specified.
use_abbreviations = {'Where do you publish your Game AI work? (in the last five years)': '('}


def file_to_content(f_path):
    """
    Processes the data in CSV files, where different answers begin with a GMT timestamp and answers to each question are
    between quotes (may be on multiple lines).
    :param f_path: path to file to process
    :return: list of question headers and answers for each question
    """
    with open(f_path) as f:
        lines = f.readlines()
        qs = lines[0].strip().split("\",\"")
        qs = [x.replace('"', '') for x in qs]
        no_questions = len(qs)-cols_skip
        ctn = [[] for _ in range(no_questions)]

        # Process all lines and put data in content list.
        answer = ""  # Variable for multi-line answers
        col_count = 0  # Current column index, reset for every new entry. Used to index content in ctn list.
        for l in range(1, len(lines)):
            line = lines[l]
            # Look for timestamp, that's a new entry. Otherwise content for 1 question is between ""
            # and may be different lines
            if re.search("[a-zA-Z0-9]* GMT", line):
                col_count = 0
                answer = ""

            if line.strip() == "":
                continue

            ans = line.split("\",\"")
            # print(line)

            if not line.startswith("\"") or line.startswith("\","):  # This is continuing answer from previous line
                answer += ans[0]
                if len(ans) > 1:  # There are more than this answer here, first add the answer and then process the rest
                    if answer != "" and col_count >= cols_skip:
                        ctn[col_count - cols_skip].append(answer)
                    col_count += 1
                    for i in range(1, len(ans)):  # Process these normally
                        a = ans[i]
                        if a.endswith("\n"):
                            answer = a  # Multi-line answer, continue to next line without increasing col count
                            continue
                        if a != "" and col_count >= cols_skip:
                            ctn[col_count - cols_skip].append(a)
                        col_count += 1
                else:  # This is the only answer, check if it's ended and if so, add it to the list.
                    if line.endswith("\"\n"):  # Line ends here
                        if answer != "" and col_count >= cols_skip:
                            ctn[col_count - cols_skip].append(answer)
                        col_count += 1

            else:  # This is a new answer
                for a in ans:
                    if a.endswith("\n") and not a.endswith("\"\n"):
                        answer = a  # Multi-line answer, continue to next line without increasing col count
                        continue
                    if a != "" and col_count >= cols_skip:
                        ctn[col_count-cols_skip].append(a)
                    col_count += 1
    return qs, ctn


questions, content = file_to_content(file_path)
no_qs = len(content)

for idx in range(no_qs):
    # Calculate a month and day for the posts, these are used for indexing (order in which they appear on the website)
    month = 11
    day = no_qs - idx + 1
    if day > 28:  # TODO: Assumes maximum 56 questions, correct if adding more
        month = 12
        day -= 28

    # Process each question based on its type and generate post and relevant plot/data
    q_title = questions[cols_skip:][idx]
    if q_types[idx] == 0:
        if q_title in use_abbreviations:
            multiple_choice(content[idx], q_title, idx, month, day, use_abbreviations[q_title])
        else:
            multiple_choice(content[idx], q_title, idx, month, day)
    elif q_types[idx] == 1:
        free_text(content[idx], q_title, idx, month, day)
    # elif q_types[idx] == 2:
    #     short_text(content[idx], questions[cols_skip:][idx], idx, month, day)
    else:
        print("Error, question type not recognized")
