import glob
import os

files = glob.glob('tests/*.py')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix _auth unpacking
    content = content.replace('access_token, _ = await register_user(client, email, "password123")', 'data = await register_user(client, email, "password123")\n    access_token = data["access_token"]')
    
    # Fix endpoint prefixes
    content = content.replace('"/auth', '"/api/v1/auth')
    content = content.replace('"/transactions', '"/api/v1/transactions')
    content = content.replace('"/onboarding', '"/api/v1/onboarding')
    content = content.replace('"/goals', '"/api/v1/goals')
    content = content.replace('"/budgets', '"/api/v1/budgets')
    content = content.replace('"/health', '"/api/v1/health')
    
    # Fix double /api/v1/api/v1 in conftest just in case
    content = content.replace('"/api/v1/api/v1', '"/api/v1')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
        
print("Tests fixed!")
