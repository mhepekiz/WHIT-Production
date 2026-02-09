-- Quick SQL script to create test data for Company Analytics Dashboard
-- Run these in Django shell: python manage.py dbshell

-- Insert test companies (sponsored ones)
INSERT OR IGNORE INTO companies_company (name, website, description, is_sponsored, is_hiring, created_at, updated_at) VALUES
('DataFlow Analytics', 'https://dataflow-analytics.com', 'Advanced data analytics platform', 1, 1, datetime('now'), datetime('now')),
('CloudTech Solutions', 'https://cloudtech-solutions.com', 'Cloud infrastructure specialists', 1, 1, datetime('now'), datetime('now')), 
('AI Innovations Lab', 'https://ai-innovations.com', 'Cutting-edge AI research', 1, 1, datetime('now'), datetime('now'));

-- Create a test recruiter user (you'll need to hash the password)
INSERT OR IGNORE INTO auth_user (username, email, first_name, last_name, is_active, is_staff, is_superuser, date_joined, password) VALUES
('test_analytics', 'analytics@test.com', 'Test', 'Analytics', 1, 0, 0, datetime('now'), 'pbkdf2_sha256$600000$test$hashedpassword');

-- Create recruiter profile  
INSERT OR IGNORE INTO recruiters_recruiter (user_id, company_name, phone, is_verified, created_at, updated_at) VALUES
((SELECT id FROM auth_user WHERE username = 'test_analytics'), 'Analytics Testing Agency', '+1-555-0123', 1, datetime('now'), datetime('now'));

-- Create company-recruiter access relationships
INSERT OR IGNORE INTO companies_companyrecruiteraccess (company_id, recruiter_id, access_level, can_see_sponsored_stats, can_manage_campaigns, can_view_analytics, can_export_data, created_at) VALUES
((SELECT id FROM companies_company WHERE name = 'DataFlow Analytics'), (SELECT id FROM recruiters_recruiter WHERE company_name = 'Analytics Testing Agency'), 'full', 1, 1, 1, 1, datetime('now')),
((SELECT id FROM companies_company WHERE name = 'CloudTech Solutions'), (SELECT id FROM recruiters_recruiter WHERE company_name = 'Analytics Testing Agency'), 'analytics', 1, 0, 1, 1, datetime('now')),
((SELECT id FROM companies_company WHERE name = 'AI Innovations Lab'), (SELECT id FROM recruiters_recruiter WHERE company_name = 'Analytics Testing Agency'), 'view', 1, 0, 1, 0, datetime('now'));

-- Create sample campaign statistics (last 7 days)
INSERT OR IGNORE INTO companies_campaignstatistics (company_id, date, page_views, unique_visitors, job_page_clicks, profile_views, application_clicks, contact_clicks, click_through_rate, engagement_rate) VALUES
-- DataFlow Analytics
((SELECT id FROM companies_company WHERE name = 'DataFlow Analytics'), date('now'), 250, 200, 75, 100, 45, 20, 0.30, 0.325),
((SELECT id FROM companies_company WHERE name = 'DataFlow Analytics'), date('now', '-1 day'), 230, 185, 70, 95, 42, 18, 0.304, 0.324),
((SELECT id FROM companies_company WHERE name = 'DataFlow Analytics'), date('now', '-2 days'), 275, 220, 82, 110, 50, 25, 0.298, 0.341),
((SELECT id FROM companies_company WHERE name = 'DataFlow Analytics'), date('now', '-3 days'), 190, 150, 55, 75, 35, 15, 0.289, 0.333),
((SELECT id FROM companies_company WHERE name = 'DataFlow Analytics'), date('now', '-4 days'), 310, 245, 95, 125, 58, 28, 0.306, 0.351),
((SELECT id FROM companies_company WHERE name = 'DataFlow Analytics'), date('now', '-5 days'), 280, 225, 85, 115, 52, 22, 0.304, 0.329),
((SELECT id FROM companies_company WHERE name = 'DataFlow Analytics'), date('now', '-6 days'), 320, 255, 98, 130, 60, 30, 0.306, 0.353),

-- CloudTech Solutions  
((SELECT id FROM companies_company WHERE name = 'CloudTech Solutions'), date('now'), 180, 145, 50, 70, 30, 12, 0.278, 0.290),
((SELECT id FROM companies_company WHERE name = 'CloudTech Solutions'), date('now', '-1 day'), 165, 132, 45, 65, 28, 10, 0.273, 0.288),
((SELECT id FROM companies_company WHERE name = 'CloudTech Solutions'), date('now', '-2 days'), 195, 155, 55, 75, 35, 15, 0.282, 0.323),
((SELECT id FROM companies_company WHERE name = 'CloudTech Solutions'), date('now', '-3 days'), 150, 120, 40, 55, 25, 8, 0.267, 0.275),
((SELECT id FROM companies_company WHERE name = 'CloudTech Solutions'), date('now', '-4 days'), 220, 175, 65, 85, 40, 18, 0.295, 0.331),
((SELECT id FROM companies_company WHERE name = 'CloudTech Solutions'), date('now', '-5 days'), 200, 160, 58, 78, 35, 16, 0.290, 0.319),
((SELECT id FROM companies_company WHERE name = 'CloudTech Solutions'), date('now', '-6 days'), 240, 190, 72, 95, 45, 20, 0.300, 0.342),

-- AI Innovations Lab
((SELECT id FROM companies_company WHERE name = 'AI Innovations Lab'), date('now'), 350, 280, 105, 140, 65, 35, 0.300, 0.357),
((SELECT id FROM companies_company WHERE name = 'AI Innovations Lab'), date('now', '-1 day'), 320, 255, 95, 130, 58, 30, 0.297, 0.345),
((SELECT id FROM companies_company WHERE name = 'AI Innovations Lab'), date('now', '-2 days'), 380, 300, 115, 155, 72, 40, 0.303, 0.373),
((SELECT id FROM companies_company WHERE name = 'AI Innovations Lab'), date('now', '-3 days'), 290, 230, 85, 115, 52, 25, 0.293, 0.335),
((SELECT id FROM companies_company WHERE name = 'AI Innovations Lab'), date('now', '-4 days'), 420, 335, 125, 170, 78, 45, 0.298, 0.367),
((SELECT id FROM companies_company WHERE name = 'AI Innovations Lab'), date('now', '-5 days'), 360, 290, 108, 145, 68, 38, 0.300, 0.366),
((SELECT id FROM companies_company WHERE name = 'AI Innovations Lab'), date('now', '-6 days'), 400, 320, 120, 160, 75, 42, 0.300, 0.366);

-- Create auth token for the test user
INSERT OR IGNORE INTO authtoken_token (key, created, user_id) VALUES 
('test_analytics_token_12345', datetime('now'), (SELECT id FROM auth_user WHERE username = 'test_analytics'));

-- Verify data creation
SELECT 'Companies created:' as result;
SELECT name, is_sponsored FROM companies_company WHERE is_sponsored = 1;

SELECT 'Recruiter created:' as result;  
SELECT u.username, r.company_name FROM recruiters_recruiter r JOIN auth_user u ON r.user_id = u.id;

SELECT 'Access relationships:' as result;
SELECT c.name as company, r.company_name as recruiter, cra.access_level 
FROM companies_companyrecruiteraccess cra 
JOIN companies_company c ON cra.company_id = c.id 
JOIN recruiters_recruiter r ON cra.recruiter_id = r.id;

SELECT 'Campaign statistics count:' as result;
SELECT c.name, COUNT(*) as stats_count 
FROM companies_campaignstatistics cs 
JOIN companies_company c ON cs.company_id = c.id 
GROUP BY c.name;