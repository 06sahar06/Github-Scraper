import streamlit as st
import requests
import time
import json

GITHUB_ACCESS_TOKEN = "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"  

MAX_PROFILES = 50
GITHUB_API_URL = "https://api.github.com"

headers = {
    'Authorization': f'token {GITHUB_ACCESS_TOKEN}'
}

def search_github_profiles(keyword, max_profiles=MAX_PROFILES):
    search_url = f"{GITHUB_API_URL}/search/users"
    params = {
        'q': keyword,
        'per_page': max_profiles,
        'sort': 'repositories',
        'order': 'desc'
    }

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['items']
    elif response.status_code == 403:
        st.write("Rate limit exceeded. Waiting...")
        reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
        time_to_wait = max(0, reset_time - time.time())
        time.sleep(time_to_wait)
        return search_github_profiles(keyword, max_profiles)
    else:
        st.write(f"Failed to search for profiles: {response.status_code}")
        return []

def fetch_profile_and_repositories(username):
    profile_url = f"{GITHUB_API_URL}/users/{username}"
    repos_url = f"{GITHUB_API_URL}/users/{username}/repos"

    profile_response = requests.get(profile_url, headers=headers)
    repos_response = requests.get(repos_url, headers=headers)

    if profile_response.status_code == 200:
        profile_data = profile_response.json()
    else:
        st.write(f"Failed to fetch profile data for {username}: {profile_response.status_code}")
        return None

    if repos_response.status_code == 200:
        repos_data = repos_response.json()
    else:
        st.write(f"Failed to fetch repositories for {username}: {repos_response.status_code}")
        repos_data = []

    return profile_data, repos_data

def analyze_profiles(profiles):
    profile_analysis = []

    for profile in profiles:
        username = profile['login']
        profile_data, repos_data = fetch_profile_and_repositories(username)

        if profile_data:
            analysis = {
                'Username': profile_data['login'],
                'Name': profile_data.get('name', 'N/A'),
                'Company': profile_data.get('company', 'N/A'),
                'Location': profile_data.get('location', 'N/A'),
                'Public Repos': profile_data['public_repos'],
                'Followers': profile_data['followers'],
                'Following': profile_data['following'],
                'Profile URL': profile_data['html_url'],
                'Repo Count': len(repos_data),
                'Top Repositories': [repo['name'] for repo in repos_data[:5]]  # Show top 5 repos
            }
            profile_analysis.append(analysis)

    return profile_analysis

def main():
    st.title("GitHub Profile Analyzer")
    keyword = st.text_input("Enter a keyword to search for profiles:")

    if keyword:
        profiles = search_github_profiles(keyword, max_profiles=MAX_PROFILES)
        profile_data = analyze_profiles(profiles)

        if profile_data:
            st.write("GitHub Profile Analysis:")
            st.json(profile_data)

            json_filename = f'github_profiles_{keyword}.json'
            with open(json_filename, 'w') as json_file:
                json.dump(profile_data, json_file, indent=4)
            st.write(f"Data saved to {json_filename}")
        else:
            st.write("No profiles found or failed to analyze.")

if __name__ == "__main__":
    main()

