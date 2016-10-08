from Config import Config
from Crawler import Crawler
from Parser import Parser

def main():
    # Configuration
    configurator = Config("./ConfigFile.xml")
    ret = configurator.config()
    
    # Crawl
    crawler = Crawler()
    crawler.crawl()

    # Parse
    parser = Parser()
    parser.parse()
    return

if __name__ == '__main__':
    main()
