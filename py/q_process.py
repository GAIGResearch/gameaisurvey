from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import re


repo_path = "../"


def multiple_choice(cnt, q_title, idx, month, day, abrev=''):
    """
    Creates post for multiple-choice type question, given answers and question title
    """
    short_title = q_title.split("(")[0].split("-")[0]
    post_title = short_title.strip().lower().replace(' ', '-')
    post_title = ''.join(e for e in post_title if e.isalnum() or e == '-')
    post_path = repo_path + "_posts/2019-" + str(month) + "-" + str(day) + "-" + post_title + ".md"
    post_frontmatter = "---\ntitle: " + short_title + "\nlayout: post\n---\n\n"

    abrev_mapping = {}

    c = []
    for con in cnt:
        con_sp = con.split(';')
        for con2 in con_sp:
            con_sp_sp = con2.split('\n')
            con_sp_sp = [x.strip() for x in con_sp_sp]
            for con3 in con_sp_sp:
                con_sp_sp_sp = con3.split(',')
                con_sp_sp_sp = [x.strip() for x in con_sp_sp_sp]
                c.extend(con_sp_sp_sp)

    # Plot word cloud
    wordcloud = WordCloud(width=300, height=300,
                          background_color='white',
                          stopwords=set(STOPWORDS),
                          prefer_horizontal=1,
                          min_font_size=4).generate(' '.join(c))
    fig = plt.figure(figsize=(3, 3), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    # plt.show()
    plt.savefig(repo_path + "assets/png/q" + str(idx) + "-wordcloud.png")
    plt.close(fig)

    # Create histogram data
    fig = plt.figure(figsize=(7, 7))
    freq = {}
    for con in c:
        abv = con
        if abrev != '' and abrev in con:
            abv = abrev + con.split(abrev)[-1]
        abv = abv.split(':')[-1].strip()
        if abv != '':
            abrev_mapping[abv] = con
            if abv in freq:
                freq[abv] = freq[abv] + 1
            else:
                freq[abv] = 1
    barp = []
    vals = list(freq.values())
    keys = list(freq.keys())
    y = np.arange(0.5, len(keys), 1)
    for con in c:
        abv = con
        if abrev != '' and abrev in con:
            abv = abrev + con.split(abrev)[-1]
        abv = abv.split(':')[-1].strip()
        if abv != '':
            barp.append(keys.index(abv))

    # Generate plot
    n, bins, patches = plt.hist(barp, orientation='horizontal', align='mid', rwidth=0.5,
                                bins=range(min(barp), max(barp) + 2, 1))
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    plt.errorbar(n, bin_centers, xerr=0.5, fmt='none', color='black')
    for i, v in enumerate(vals):
        # Count percentage of responses including this
        total = len(cnt)
        count = 0
        for con in cnt:
            if keys[i] in con:
                count += 1
        perc = round(count * 100.0 / total, 2)
        plt.text(v + 1, y[i] - 0.1, str(v) + " (" + str(perc) + "%)")
    plt.yticks(y, [''.join(e for e in k if e.isalnum() or e in '- ') for k in keys])
    plt.xlim(0, max(vals) + 10)
    plt.ylim(0, max(barp) + 1)

    # Recolor bars to colormap values
    cm = plt.cm.get_cmap('rainbow')
    col = bin_centers - min(bin_centers)  # scale values to interval [0,1]
    col /= max(col)
    for cl, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(cl-0.1))

    # plt.show()
    plt.tight_layout()
    plt.savefig(repo_path + "assets/png/q" + str(idx) + ".png")
    plt.close(fig)

    # Spell out all content if abbreviated in plot
    spelled_out = ''
    if abrev != '':
        spelled_out = '\n\n'
        for key in keys:
            spelled_out += '* ' + abrev_mapping[key] + '\n'

    # Create post
    post_content = "### " + q_title + \
                   "\n\n\n<center><img src='assets/png/q" + str(idx) + ".png' /></center>" + spelled_out + \
                   "\n\n<hr><center><img src='assets/png/q" + str(idx) + "-wordcloud.png' /></center>"
    with open(post_path, 'w+') as f:
        f.write(post_frontmatter + post_content)


def free_text(cnt, q_title, idx, month, day):
    """
    Creates post for free text (long text) type question, given answers and question title
    """
    short_title = q_title.split("(")[0].split("-")[0]

    post_title = short_title.strip().lower().replace(' ', '-')
    post_title = ''.join(e for e in post_title if e.isalnum() or e == '-')
    post_path = repo_path + "_posts/2019-" + str(month) + "-" + str(day) + "-" + post_title + ".md"
    post_frontmatter = "---\ntitle: " + short_title + "\nlayout: post\n---\n\n"

    # Plot word cloud
    wordcloud = None
    try:
        wordcloud = WordCloud(width=300, height=300,
                              background_color='white',
                              stopwords=set(STOPWORDS),
                              prefer_horizontal=1,
                              min_font_size=4).generate(' '.join(cnt))
        fig = plt.figure(figsize=(3, 3), facecolor=None)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        # plt.show()
        plt.savefig(repo_path + "assets/png/q" + str(idx) + "-wordcloud.png")
        plt.close(fig)
    except:
        print("Worldcloud error")

    # Process urls and split answers by '\n'
    c = []
    for con in cnt:
        link = re.findall('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', con)
        links = [x[0] + "://" + x[1] + x[2] for x in link]
        cc = con
        for l in links:
            cc = cc.replace(l, "[<a href='" + l + "'>url</a>]")
        con_sp = cc.split('\n')
        c.extend(con_sp)

    # Check if answers repeat (or are included in other answers)
    illegal = []
    for cn1 in range(len(c)):
        for cn2 in range(len(c)):
            if cn1 != cn2:
                con1 = c[cn1]
                con2 = c[cn2]

                keep1 = True
                keep2 = True
                if con1.lower().strip() == con2.lower().strip():
                    keep1 = True
                    keep2 = False
                if con1.lower().strip() in con2.lower().strip():
                    keep1 = False
                    keep2 = True
                elif con2.lower().strip() in con1.lower().strip():
                    keep1 = True
                    keep2 = False
                if not keep1 and con1 not in illegal:
                    illegal.append(con1)
                if not keep2 and con2 not in illegal:
                    illegal.append(con2)
    for con in illegal:
        while con in c:
            c.remove(con)

    # Capitalize first letter of each item
    capitalized = [re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), x, 1).strip() for x in c]
    if '' in capitalized:
        capitalized.remove('')

    # Create post
    post_content = "### " + q_title + ("\n\n* " if len(capitalized) > 0 else '') + \
                   "\n* ".join(capitalized) + \
                   ("\n\n<hr><center><img src='assets/png/q" + str(idx) + "-wordcloud.png' /></center>"
                    if wordcloud is not None else '')
    with open(post_path, 'w+') as f:
        f.write(post_frontmatter + post_content)

