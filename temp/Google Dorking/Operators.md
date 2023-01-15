# Operators

## site

Tells Google to show you results from a certain site only. This will help you quickly find the most reputable source on the topic that you are researching. For example, if you wanted to search for the syntax of Python’s `print()` function, you could limit your results to the official Python documentation with this search: `print site:python.org`.

## inurl

Searches for pages with a URL that match the search string. It’s a powerful way to search for vulnerable pages on a particular website. Let’s say you’ve read a blog post about how the existence of a page called */course/jumpto.php* on a website could indicate that it’s vulnerable to remote code execution. You can check if the vulnerability exists on your target by searching `inurl:"/course/jumpto.php" site:example.com`.

## intitle

Finds specific strings in a page’s title. This is useful because it allows you to find pages that contain a particular type of content. For example, file-listing pages on web servers often have *index of* in their titles. You can use this query to search for directory pages on a website: `intitle:"index of" site:example.com`*.*

## link

Searches for web pages that contain links to a specified URL. You can use this to find documentation about obscure technologies or vulnerabilities. For example, let’s say you’re researching the uncommon regular expression denial-of-service (ReDoS) vulnerability. You’ll easily pull up its definition online but might have a hard time finding examples. The link operator can discover pages that reference the vulnerability’s Wikipedia page to locate discussions of the same topic: link:"https://en.wikipedia.org/wiki/ReDoS".

## filetype

Searches for pages with a specific file extension. This is an incredible tool for hacking; hackers often use it to locate files on their target sites that might be sensitive, such as log and password files. For example, this query searches for log files, which often have the *.log* file extension, on the target site: `filetype:log site:example.com`.

## Wildcard (*)

You can use the wildcard operator (`*`) within searches to mean *any character or series of characters*. For example, the following query will return any string that starts with *how to hack* and ends with *using Google*. It will match with strings like *how to hack websites using Google*, *how to hack applications using Google*, and so on: `"how to hack * using Google"`.

## Quotes (" ")

Adding quotation marks around your search terms forces an exact match. For example, this query will search for pages that contain the phrase *how to hack*: `"how to hack"`. And this query will search for pages with the terms *how*, *to*, and *hack*, although not necessarily together: `how to hack`.

## Or (|)

The or operator is denoted with the pipe character (`|`) and can be used to search for one search term or the other, or both at the same time. The pipe character must be surrounded by spaces. For example, this query will search for *how to hack* on either Reddit or Stack Overflow: `"how to hack" site:(reddit.com | stackoverflow.com)`. And this query will search for web pages that mention either *SQL Injection* or *SQLi*: `(SQL Injection | SQLi)`. *SQLi* is an acronym often used to refer to SQL injection attacks, which we’ll talk about in Chapter 11.

## Minus (-)

The minus operator (-) excludes certain search results. For example, let’s say you’re interested in learning about websites that discuss hacking, but not those that discuss hacking PHP. This query will search for pages that contain how to hack websites but not php: "how to hack websites" -php.

## Ex

site:\*.example.com
site:example.com inurl:app/kibana
site:s3.amazonaws.com COMPANY_NAME
site:example.com ext:php
site:example.com ext:log
site:example.com ext:txt password

## References

<https://www.exploit-db.com/google-hacking-database/>
