# 🌟 Welcome to our A/B Testing Group Project Documentation  

This site provides comprehensive documentation for setting up, running, and maintaining our A/B Testing project. Whether you're a developer, data scientist, or stakeholder, you'll find everything you need to understand and utilize the system effectively.

---

## 📂 Project Structure  

Here’s a quick look at the project’s organization:

- **Database**: Postgres database.
- **API**: Fast API that connects with the Postgres database.
- **App**: Streamlit application that connects with the Fast API.
- **PgAdmin**: UI tool that shows you the data you've inserted and helps with database management.
- **Docs**: MkDocs documents your codebase and project setup for easy understanding.

---

# 🧠 Project Overview

## Problem 😵‍💫  
In the world of streaming platforms, competition is fierce, especially when you're a movie streaming service with only about a dozen *very cliché* movies that could probably be found for free on any random website. Keeping customers engaged, loyal, and willing to pay is a challenge—especially when you're squeezing every last drop of value out of content that's been circulating since dial-up internet. 🎥🕰️  

## Solution? 🚀  
Enter our new *customer extraction—er, engagement tool*! This system lets us squeeze... I mean, *enhance* customer loyalty and monetization by understanding their behavior better. Here's how it works:  

### 1. Customer Segmentation 🤹‍♀️  
We take our users and sort them into segments based on their viewing habits and engagement levels. For example:  
- How frequently they engage with our platform.  
- Their viewing habits and interaction patterns.  

Based on these insights, customers are segmented into four groups:  
- **Lost Cause**: Users who show minimal or no interest in our platform.  
- **Vulnerable Customers**: Users who engage somewhat but are at risk of leaving.  
- **Free Riders**: Users who consume content but avoid paying.  
- **Star Customers**: Loyal and engaged users who are the backbone of our platform.  
  
### 2. A/B Testing 🔍📩  
The fun part! We divide these segments in half and send each group different emails. For example:  
- **Group A** gets, "You deserve the best, and the Basic plan gives you just that—for only 10 dollars. Start your premium experience today! Click here to learn more: [the link]"
- **Group B** gets, “Simple. Affordable. Amazing. The Basic plan is yours today for just 10 dollars. What are you waiting for? Click here to learn more:[the link]” 

By monitoring engagement—who opens the emails, clicks the links-we figure out which message gets more attention. 👀💡  

### 3. Backend API 🖥️💾  
A powerhouse that manages everything from assigning segments to sending these *brilliantly persuasive* emails to tracking the results.  

### 4. Frontend Dashboard 📊✨  
A fun little tool (built with Streamlit) that lets us track results, identify trends, and brainstorm the next way to charm our users into staying.  

# Expected Outcome 🎯  
With this system, we’re expecting to:  
1. Better categorize our customers (maybe even discover who’s still here just for nostalgia). 🤔📂  
2. Test marketing tactics that make “Premium for $10” sound like the *deal of the century*. 💸✨  
3. Increase customer engagement (even if that means getting them to complain about our emails—at least they’re interacting, right?). 🗨️  
4. Ultimately, convince customers (at least those who are real) that they can’t live without us, no matter how basic we are. 🎞️🎉  

This tool ensures we stay one step ahead of our competitors (or at least cling to our existing audience while pretending our content isn’t free everywhere else). By the time we’re done, we might just make them love us as much as we love their subscription payments. 🫶💵
