## SEcured REcorder BOx (SEREBO) - Secured Data Logger Based on Blockchain Technology
**Problem scenario:** I am a researcher and I often generate data files as I go about my work. Take for example, an Excel file, sampleTimeSeries.xlsx, that I had generated on 15th May 2015. Three years later on 10th June 2018, how can I demonstrate that sampleTimeSeries.xlsx had not been changed / edited since 15th May 2015? If I had the intention to change the file on 10th December 2016, I can safely set my computer clock back to 15th May 2015, change the file, and the date will still be 15th May 2015.

**Solution:** What if there is a way for me to log my file into a system, on 15th May 2015, and this record (the log statement) is not editable? To ensure that this record is not editable, it can be put on a blockchain. One of the most useful features of a blockchain is resistance against modification of data.

This is where I thought of the concept of a data recorder based on blockchain and **SEcured REcorder BOx (SEREBO)** is born. The term "secured" refers to security against amendments or modifications rather than security against data theft. SEREBO consists of two components for secured data logging - **SEREBO Black Box** and **SEREBO Notary**.

## SEREBO Black Box
SEREBO Black Box is inspired by the black boxes (cockpit voice recorder and flight data recorder) in airliners. The intended purpose is to track and audit research records under the following premise - Given a set of data files, is there a system to log and verify that these files had not been changed or edited since its supposed creation?

SEREBO Black Box aims to address this issue by using several approaches. Firstly, the data files can be used to generate a file hash. It is very likely that an edit in the file will result in a different hash. Hence, if a file generates the same hash across two different points in time, it can be safely assumed that the file had not been edited during this time span. Secondly, the file hash has to be securely recorded with amendment protected. SEREBO records the hash and registers the hash into a blockchain. The main concept of blockchain is that the hash of previous (parent) block is concatenated with the data (file hash in this case) of the current block to generate a hash for the current block. Hence, as the blockchain grows, any amendments in earlier blocks can be easily detected - only amendments to the latest block cannot be detected. Therefore, the value of SEREBO lies in its use.

## SEREBO Notary
SEREBO Black Box, in itself, is insufficiently secured from modifications by the fact that it is a standalone unit. An easy method to increase the level of security is to have SEREBO Black Boxes periodically notarized by one or more independent notary / notaries. SEREBO Notary is a web application built on Web2Py framework and exposes a set of XMLRPC web services so as to provide an independent agent / platform as a notary service.

## How to Cite SEREBO
If you used SEREBO, please cite the following source(s):
* Ling, MHT. 2018. [SEcured REcorder BOx (SEREBO) Based on Blockchain Technology for Immutable Data Management and Notarization.](https://github.com/mauriceling/mauriceling.github.io/wiki/SEcured-REcorder-BOx-%28SEREBO%29-Based-on-Blockchain-Technology-for-Immutable-Data-Management-and-Notarization.) MOJ Proteomics & Bioinformatics 7(6):169‒174.
