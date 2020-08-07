# Assignment 12

I was able to get the GPFS running but the crawling the reddit url was taking a very long time to complete and it's still going after two days. I don't think it will finished before end of day today, so I'm submitting my progress.

1. How much disk space is used after step 4?

> as of now it has used 21G

2. Did you parallelize the crawlers in step 4? If so, how?

> I noticed that different years has different average size of url files. That is some years have more links to crawl that others; whereas, within the same year, the url.txt file sizes are similar. In order to minimize bottleneck, I parallelized the process by month. I had 12 crawlers running at the same time with each one crawling all of the files of the same month. Since I have three nodes, I ran four crawlers on each node.

3. Describe the steps to de-duplicate the web pages you crawled.

>  The downloaded pages were depulicated by the number of overlapping n-grams. If the overlap passes the threshold, the a page will be placed onto the duplicated list.

4. Submit the list of files you that your LazyNLP spiders crawled (ls -la).

> list of files downloaded for aus_gutenberg: https://github.com/erikhou45/w251-assignments/blob/master/hw12/aus_gutenberg_ls

> list of files downloaded for us_gutenberg: https://github.com/erikhou45/w251-assignments/blob/master/hw12/us_gutenberg_ls
