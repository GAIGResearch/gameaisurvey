from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

stop_words = STOPWORDS
stop_words.add("base")
stop_words.add("based")
stop_words.add("method")
stop_words.add("methods")
stop_words.add("technique")
stop_words.add("techniques")
stop_words.add("approach")
stop_words.add("approaches")
stop_words.add("algorithm")
stop_words.add("algorithms")
stop_words.add("apply")
stop_words.add("applied")
stop_words.add("automated")
stop_words.add("problem")
stop_words.add("problems")
stop_words.add("advance")
stop_words.add("advanced")
stop_words.add("relate")
stop_words.add("related")
stop_words.add("recent")
stop_words.add("success")
stop_words.add("successfully")
stop_words.add("big")
stop_words.add("biggest")
stop_words.add("small")
stop_words.add("field")
stop_words.add("domain")
stop_words.add("area")
stop_words.add("towards")
stop_words.add("thus")
stop_words.add("making")
stop_words.add("hard")
stop_words.add("easy")
stop_words.add("better")
stop_words.add("worse")
stop_words.add("see")
stop_words.add("huge")
stop_words.add("ex")
stop_words.add("page_id")
stop_words.add("site")
stop_words.add("sites")
stop_words.add("plt")
stop_words.add("ode")
stop_words.add("large")
stop_words.add("available")
stop_words.add("arxiv")
stop_words.add("vol")
stop_words.add("abs")
stop_words.add("pdf")
stop_words.add("document")
stop_words.add("preprint")
stop_words.add("many")
stop_words.add("etc")
stop_words.add("index")
stop_words.add("https")
stop_words.add("href")
stop_words.add("www")
stop_words.add("net")
stop_words.add("com")
stop_words.add("edu")
stop_words.add("org")
stop_words.add("ovgu")
stop_words.add("dke")
stop_words.add("eecs")
stop_words.add("crc")
stop_words.add("uma")
stop_words.add("info")
stop_words.add("dspace")
stop_words.add("ritsumei")
stop_words.add("ice")
stop_words.add("mun")
stop_words.add("home")
stop_words.add("nyu")
stop_words.add("qmul")
stop_words.add("events")

stop_words.add("github")
stop_words.add("conference")
stop_words.add("journal")
stop_words.add("ieeexplore")
stop_words.add("paper")
stop_words.add("papers")
stop_words.add("page")
stop_words.add("two")
stop_words.add("html")
stop_words.add("book")
stop_words.add("school")
stop_words.add("google")
stop_words.add("youtube")
stop_words.add("summer")
stop_words.add("edition")
stop_words.add("second")
stop_words.add("first")

stop_words.add("game")
stop_words.add("games")


def generate_wordcloud(text):
    return WordCloud(width=300, height=300,
                     background_color='white',
                     stopwords=set(stop_words),
                     prefer_horizontal=1,
                     min_word_length=3,
                     min_font_size=4).generate(text)


def save_wordcloud_fig(cloud, f_name):
    fig = plt.figure(figsize=(3, 3), facecolor=None)
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    # plt.show()
    plt.savefig(f_name)
    plt.close(fig)


def wordcloud_from_file(f_name_from, f_name_to):
    with open(f_name_from) as f:
        text = f.read()
        cloud = generate_wordcloud(text)
        save_wordcloud_fig(cloud, "png/" + f_name_to)


wordcloud_from_file("content.txt", "cloud1.png")
