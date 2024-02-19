# Design Email

## Topics

1. How to send email?
2. How to send email in real time?
3. How to store attachments?
4. How to scale websocket service?
5. Check spams?
6. Search emails?

## Functional Requirements:

1. User can send and receive emails.
2. User can receive email in real time?
3. User can attach files in an email.

## Non-functional requirements:

1. Low latency
2. Highly available

## API

```
v1/send POST

json {
  uid
  email title
  recipients
  email body
}

response: 201 OK

v1/emails GET
json {
  uid
  page_number,
  page_size
}

Response:
[
  Email1: {},
  Email2: {},
  ...
]

websocket API for getting push notification and auto refresh of email list.
/connect 

/email
data: 
```

## Data Schema

```
User {
  uid: uuid,
  name: string,
  email: string,
  profile_url: string,
}

Email {
  id: uuid,
  uid: uuid,
  recipients: []string,
  subject: string,
  attachments: []string, // files stored in file storage
  body: TEXT,
}
```

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (24).svg" alt="" class="gitbook-drawing">

1. A user write email on webmail and press send button. The request is sent to load balancer.
2. The load balancer makes sure it doesn't exceed rate limit and routes traffic to web servers.
3. Web servers responsible for:
   1. Basic email validation, like email size limit.
   2. Check if domain of recipient email is the same as sender. If it is the same, the web server ensures the email data is spam and virus free. If so, email is stored in sender's sent folder and inbox folder directly without sending to outgoing queue.
4. Message queues
   1. If basic email validation succeeds, the email data is passed to the outgoing queue.&#x20;
   2. If basic email validation fails, the email is put in the error queue.
5. SMTP outgoing workers pull messages from the outgoing queue and make sure emails are spam and virus free.&#x20;
6. The outgoing email is stored in the sent folder of storage.
7. SMTP outgoing workers send the email to recipient mail server.

## Email deliverability & Spam

<mark style="color:purple;">Dedicated IPs:</mark>

Recommended to have dedicated IP addresses for sending emails. Email providers are less likely to accept email from new IP addresses that have no history.

<mark style="color:purple;">Classify emails</mark>

Send different categories of emails from different IP addresses. For example, you may want to avoid sending marketing and other important emails from the same servers because it might make ISPs mark all emails as promotional.

<mark style="color:purple;">Email sender reputation</mark>

Warm up new email server IP addresses slowly to build a good reputation. so big providers like Office365, Gmail and Yahoo Mail are less likely to put our emails in the spam folder. takes 2-6 weeks to warm up new IP address.

<mark style="color:purple;">Ban spammers quickly</mark>

Spammers should be banned quickly before they have a significant impact on server's reputation.

<mark style="color:purple;">Feedback processing</mark>

It's very important to set up feedback loops with ISPs so we can keep complaint rate low and ban spam quickly.&#x20;

Hard bounce: an email is rejected by ISP because the recipient's email is invalid.

Soft bounce: A soft bounce indicates an email failed to deliver due to temporary conditions, such as ISPs being too busy.

Complaint: A recipient clicks the report spam button.

<img src="../../.gitbook/assets/file.excalidraw (22).svg" alt="" class="gitbook-drawing">

## Search

<table><thead><tr><th width="155">Search</th><th>Scope</th><th>Sorting</th><th>Accuracy</th></tr></thead><tbody><tr><td>Google search</td><td>The whole internet</td><td>Sort by relevance</td><td>Indexing generally takes time, so some items may not show in the search result immediately.</td></tr><tr><td>Email search</td><td>User's own email box</td><td>Sort by attributes such as time, has attachment, date within, is unread, etc.</td><td>Indexing should be near real-time, and the result has to be accurate.</td></tr></tbody></table>

### Option 1: Elastic search

<img src="../../.gitbook/assets/file.excalidraw (23).svg" alt="" class="gitbook-drawing">

### Option 2: Custom search solution using LSM

## Email 101

SMTP:&#x20;

Simple Mail Transfer Protocol (SMTP) standard protocol for sending emails from one email server to another.

POP:

standard mail protocol to receive and download emails from a remote mail server to a local email client. Once emails are downloaded to your computer/phone, they are deleted from email server.

IMAP:

standard mail protocol for receiving emails for a local email client. When you read an email, you are connected to an external mail server, and data is transferred to your local device. IMAP only downloads message when you click it, and emails are not deleted from mail servers.&#x20;
