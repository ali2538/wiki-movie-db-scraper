from typing import Iterable
import scrapy
import re
import time
import pandas as pd


class WikiMovieListSpider(scrapy.Spider):
    name = "wiki_movie_db"
    allowed_domains = ["en.wikipedia.org"]

    def start_requests(self):
        initial_list = pd.read_csv("../movie_titles_and_their_wiki_links.csv")
        urls = initial_list["wiki_link"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        wikipedia_link = response.url

        def clean_up(cur_list):
            superscript = re.compile("\[[0-9a-zA-Z]+\]")
            new_list = []
            for w in cur_list:
                if (
                    (w == "\n")
                    or (".mw-parser-output" in w)
                    or (".plainlist" in w)
                    or (":" in w)
                    or superscript.match(w)
                ):
                    pass
                else:
                    new_list.append(w)
            return new_list

        def pick_dates(cur_list):
            all_digit_date_format = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
            new_list = []
            for w in cur_list:
                if all_digit_date_format.match(w):
                    new_list.append(w)
            if not new_list:
                new_list = cur_list
            return new_list

        def currency_cleanup(cur_list):
            new_list = []
            for w in cur_list:
                if "$" in w:
                    new_list.append(w)
            if not new_list:
                new_list = cur_list
            return new_list

        movie_title = response.xpath(".//header/h1/i/text()").extract()
        movie_title_part_02 = response.xpath(".//header/h1/text()").extract()
        if movie_title_part_02:
            movie_title = movie_title + movie_title_part_02
        directors = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Directed by')]/following-sibling::td//text()"
            ).extract()
        )

        writers = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Screenplay by')]/following-sibling::td//text()"
            ).extract()
        )
        if not writers:
            writers = clean_up(
                response.xpath(
                    ".//th[contains(text(), 'Written by')]/following-sibling::td//text()"
                ).extract()
            )

        story_by = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Story by')]/following-sibling::td//text()"
            ).extract()
        )

        producers = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Produced by')]/following-sibling::td//text()"
            ).extract()
        )

        starring = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Starring')]/following-sibling::td//text()"
            ).extract()
        )

        cinematography = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Cinematography')]/following-sibling::td//text()"
            ).extract()
        )

        editors = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Edited by')]/following-sibling::td//text()"
            ).extract()
        )

        music_by = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Music by')]/following-sibling::td//text()"
            ).extract()
        )

        production_companies = clean_up(
            response.xpath(
                ".//div[contains(text(), 'Production')]/../following-sibling::td//text()"
            ).extract()
        )

        distributed_by = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Distributed by')]/following-sibling::td//text()"
            ).extract()
        )

        release_dates = clean_up(
            response.xpath(
                ".//div[contains(text(), 'Release date')]/../following-sibling::td//text()"
            ).extract()
        )
        release_dates = pick_dates(release_dates)

        running_time = clean_up(
            response.xpath(
                ".//div[contains(text(), 'Running time')]/../following-sibling::td//text()"
            ).extract()
        )

        countries = clean_up(
            response.xpath(
                ".//th[re:match(text(), 'Countr[yies]{0,3}')]//following-sibling::td//text()"
            ).extract()
        )

        languages = clean_up(
            response.xpath(
                ".//th[re:match(text(), 'Languages?')]//following-sibling::td//text()"
            ).extract()
        )

        budget = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Budget')]/following-sibling::td//text()"
            ).extract()
        )
        budget = currency_cleanup(budget)

        box_office = clean_up(
            response.xpath(
                ".//th[contains(text(), 'Box office')]/following-sibling::td//text()"
            ).extract()
        )
        box_office = currency_cleanup(box_office)

        imdb_link = response.xpath(
            ".//a[contains(text(), 'IMDb')]/preceding-sibling::a/@href"
        ).extract()
        time.sleep(10)
        yield {
            "movie_title": movie_title,
            "directors": directors,
            "writers": writers,
            "story_by": story_by,
            "producers": producers,
            "starring": starring,
            "cinematography": cinematography,
            "editors": editors,
            "music_by": music_by,
            "production_companies": production_companies,
            "distributed_by": distributed_by,
            "release_dates": release_dates,
            "running_time": running_time,
            "countries": countries,
            "languages": languages,
            "budget": budget,
            "box_office": box_office,
            "wikipedia_link": wikipedia_link,
            "imdb_page": imdb_link,
        }
