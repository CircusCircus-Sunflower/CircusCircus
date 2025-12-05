# CircusCircus Project: Week-Long Flask Forum Enhancement

## Project Overview

Students will be working with **CircusCircus**, a minimal forum application built with Python Flask. 
This project serves as an excellent way to internalize _adding new features_ to an exisitng system 
that combines web development fundamentals, database management, 
collaborative development practices, and real-world software enhancement skills.

This is a group project, requiring Lots of communication among the group members.

## What Students Will Learn

### **Core Technical Skills**

- **READ what is already in the system** Don't try to add to something you don't understand
- **Flask Web Framework**: Working with routes, templates, forms, and session management
- **Database Migration**: Moving from SQLite to MySQL, understanding database design and relationships
- **Code Modularization**: Refactoring a monolithic application into organized, maintainable modules
- **Front-end Integration**: Implementing responsive design with Bootstrap and handling media content
- **API Development**: Building features like direct messaging and emoji reactions

### **Professional Development Skills**
- **Git Collaboration**: Managing branches (main, dev, individual feature branches)
- **Team Coordination**: Working as collaborators on a shared GitHub organization repository  
- **Project Planning**: Breaking down complex features into manageable tasks
- **Code Review**: Reviewing and integrating team members' contributions

### **Software Architecture Concepts**
- **Separation of Concerns**: Dividing functionality into modules (posts, comments, auth)
- **Database Relationships**: Implementing one-to-many relationships (posts to comments)
- **User Permission Systems**: Public vs private post visibility
- **Content Management**: Handling text, markdown, images, and video links

## Top Focus Areas for the Week

### **Days 1-2: Foundation & Setup**
**Priority 1: Environment & Collaboration**
- Set up the development environment (Python 3.11+, virtual environment)
- Create GitHub organization and configure team collaboration
- Establish branch strategy (main, dev, individual branches)
- Get the existing application running locally

**Priority 2: Code Organization**
- **Critical Focus**: Refactor `forum.py` into logical modules:
  - `auth.py` (login, registration, session management)
  - `posts.py` (thread creation, viewing, editing)
  - `comments.py` (comment functionality)
- This modularization is fundamental to all future enhancements

### **Days 3-4: Core Enhancements**
**Priority 3: Database Migration**
- Migrate from SQLite to MySQL
- Understand database connection management
- Test data persistence and relationships

**Priority 4: Essential Features**
- Implement comments system (many-to-one relationship with posts)
- Add emoji reactions (like/dislike/heart) to posts
- Focus on proper database schema design for these features

### **Days 5-7: Advanced Features & Polish**
**Priority 5: User Experience**
- Implement public/private post visibility
- Add markdown support for post formatting
- Create user settings functionality

**Priority 6: Professional Presentation**
- Apply Bootstrap styling for responsive design
- Add logo and consistent branding
- Implement footer with copyright and about information
- Handle image/video link embedding

**Priority 7: Advanced Communication**
- Direct messaging between users (if time permits)
- This is the most complex feature - attempt only after core functionality is solid

## Success Metrics

**Minimum Viable Product (MVP)**:
- Modularized codebase with separate auth, posts, and comments modules
- MySQL database integration working
- Comments functionality operational
- Basic Bootstrap styling applied

**Stretch Goals**:
- Public/private post system working
- Emoji reactions functional
- Direct messaging implemented
- Professional styling with logo and footer

## Daily Checkpoint Questions

**For Students**: Each day, ask yourself:
1. "Can I explain how this feature connects to the overall architecture?"
2. "How does this change affect other team members' work?"
3. "What would break if we removed this component?"

**For Instructors**: Monitor:
- Are teams effectively using Git branching?
- Is the code modularization logical and clean?
- Are database relationships properly implemented?

## Key Learning Outcomes

By the end of this week, students will have experienced the full cycle of collaborative software development: taking existing code, understanding its architecture, planning enhancements, implementing features as a team, and delivering a polished product. This mirrors real-world development scenarios where teams inherit and improve existing codebases rather than building from scratch.

The project emphasizes **practical skills** over theoretical concepts, giving students tangible experience with tools and workflows they'll use in their careers.
