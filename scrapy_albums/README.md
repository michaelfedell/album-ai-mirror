# Scrapy Job

This part of the project defines a web-scraping job to pull data from AlbumOfTheYear.org, collecting information on all top albums available for ever genre across the past several decades.

## Quick Guide

Although scrapy is a great framework that makes many parts of the web scraping workflow very easy, it does have a bit of a learning curve. You can find more about scrapy [here](https://docs.scrapy.org/en/latest/intro/tutorial.html), but the following will provide a quick reference for tweaking/running this project:

### Spiders

Spiders are the python objects which will crawl a webpage and return data or further requests to follow/process. They are defined in `scrapy_albums/spiders`, currently only a single spider is used, defined in [genrecrawl.py](scrapy_albums/spiders/genrecrawl.py). This spider will start on the [genre homepage]('https://www.albumoftheyear.org/genre.php') to scrape all available genres, then crawl all listed albums for each decade in those genres.

### Settings

To change how the scrapy job runs, you can tweak [various settings](scrapy_albums/settings.py) such as `DOWNLOAD_DELAY` and `CONCURRENT_REQUESTS_PER_DOMAIN` to control speed of job. Currently the job is set up to run rather at a moderate pace so that the website is not overwhelmed with requests. 

### Running

To start the job, you must first install scrapy (recommended to install within a virtualenv or conda env due to large dependency web).

```shell
conda install scrapy
```

Once installed, navigate to this directory from command line

```shell
cd path/to/scrapy_albums
```

To start the crawl, run:

```shell
scrapy crawl genrecrawl -o <local_output_file>.jl
```

A detailed log will be saved in the current working directory as `scrapy_output.log`, and the results will be saved to `<local_output_file>.jl` specified when command was run.

**WARNING**: if an existing `.jl` file is passed, the new results will be appended to this file.