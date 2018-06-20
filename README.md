# SEcured REcorder BOx (SEREBO)
SEREBO (SEcured REcorder BOx) consists of two components for secured data logging - **SEREBO Black Box** and **SEREBO Notary**. The term "secured" refers to security against amendments rather than security against data theft.

## SEREBO Black Box
SEREBO Black Box is inspired by the black boxes (cockpit voice recorder and flight data recorder) in airliners. The intended purpose is to track and audit research records under the following premise - Given a set of data files, is there a system to log and verify that these files had not been changed or edited since its supposed creation?

SEREBO Black Box aims to address this issue using several approaches. Firstly, the data files can be used to generate a file hash. It is very likely that an edit in the file will result in a different hash. Hence, if a file generates the same hash across two different points in time, it can be safely assumed that the file had not been edited during this time span. Secondly, the file hash has to be securely recorded with amendment protected. SEREBO records the hash and registers the hash into a blockchain. The main concept of blockchain is that the hash of previous (parent) block is concatenated with the data (file hash in this case) of the current block to generate a hash for the current block. Hence, as the blockchain grows, any amendments in earlier blocks can be easily detected - only amendments to the latest block cannot be detected. Therefore, the value of SEREBO lies in its use.


## SEREBO Notary
