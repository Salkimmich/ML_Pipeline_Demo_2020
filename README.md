## Data Science Design Document 

### Developer Contact

Technical PoC: Sara Kimmich

### Contents:

1. Introduction
2. Data Science Scope
    2a. Business Case
    2b. Key User Stories
3. Data
4. Feature Engineering
5. Machine Learning Model
6. Training and Tuning
7. Data Visualization 
8. Testing
9. Ethical/Legal Compliance
10. Cloud Integration

## 2. Data Science Scope

### Business Case 

#### Pain Point: 
#### Machine Learning Application: 
#### Model Success: 

### Key User Stories

## 3. Data
## 4. Feature Engineering
#### Alternative Methods/Models: 

## 5. Machine Learning Model: 
#### Model Performance:
#### Prediction Scores
#### Alternative Methods/Models: 

## 6. Training and Tuning
### Tunable Parameters

## 7. Data Visualization

## 8. Testing
##### Cross-Validation

## 9. Ethical/Legal Compliance

##### Database as a Service:
1. What information is being collected?
2. Who is collecting it?
3. Why is it being collected? 
4. How will it be used?
5. Who will it be shared with?
6. What will be the effect of this on the individuals concerned?
7. Is the intended use likely to cause individuals to object or complain? 

##### Software as a Service: GDPR Checklist
1. Write down your risk assessments to make your data safe
2. **Have a process in place for timely deleting data when requested
3. What data is stored? Know what personal data are you storing and why? Personal Data is any information that could be used to identify a person (name, phone, IP address)
4. Don't hold onto data with no known use (you can't hold onto data unless you know what you are going to do with it and have it written down
5. What measures do you have in place to make sure your data is secured?


## 9. Cloud Integration 

*Further testing and integration with larger DevOps ecosystem to be defined and discussed in future scope of work with client.*

1. Initial client communication seeks to ensure that a shared understanding of what kind of optimization strategy would be most effective. This is typically established by defining one or more 1) problem statement, 2) business case/user story, and 3) technical solution model. This format allows for evaluation of optimization success either behavioral testing via the user story and/or a unit test evaluation for the technical solution model.

2. Establish architectural diagrams at the level of System Context (who/what accesses and why) as well as a container diagram for each application which clearly delineates each point of the application interface. This very effectively establishes the ground truth of what the system is, as well as what the client would like to optimize the system to be - even if they don’t quite know the answer to that question themselves. This process usually takes only about 30 minutes to establish basic architectural diagrams, depending on the complexity of dependencies. 
 
3. Audit of current AWS service ecosystem using Cost Explorer, usually with the client on hand to walk through usage and establish any predictable resourcing patterns to be leveraged. Depending on the sophistication of the client’s system there may already be some cost categories that will be tied to the architectural diagrams to establish a visual and narrative understanding of system usage. 

These steps allow for a baseline understanding of total usage, and any further optimization either strictly through AWS services (often more effective scaling) or via architectural reconfiguration of the application to streamline overall CPU usage of the services. 



