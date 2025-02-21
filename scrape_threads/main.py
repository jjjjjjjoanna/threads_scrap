import asyncio
import csv

from scrape_threads import scrape_profile, scrape_thread

async def main():
    # thread_url = "https://www.threads.net/@peter_and_susan/post/DC1VRJcvZE_"
    # profile_url = "https://www.threads.net/@lazyhongram"
    
    # thread_data = await scrape_thread(thread_url)
    # print("Thread Data:", thread_data)


    authors = []
    with open('authors_data.csv', 'r', encoding='utf-8') as authors_file:
        reader = csv.DictReader(authors_file)
        for row in reader:
            authors.append(row['user'])
    profile_results = []

    for author in authors:
        profile_url = f"https://www.threads.net/@{author}"
        print(f"Scraping profile for: {profile_url}")
        
        try:
            profile_data = await scrape_profile(profile_url)
            profile_results.append(profile_data)
        except Exception as e:
            print(f"Error scraping {profile_url}: {e}")

    with open('profiles_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'full_name', 'bio', 'followers', 'bio_links', 'url'])
        writer.writeheader()

        for profile_data in profile_results:
            writer.writerow(profile_data['user'])

    with open('threads_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'username', 'code', 'text', 'published_on', 'has_audio', 'reply_count', 'like_count', 'image_count', 'images', 'url'])
        writer.writeheader()

        for profile_data in profile_results:
            for thread in profile_data['threads']:
                writer.writerow(thread)

    # profile_data = await scrape_profile(profile_url)

    # with open('profile_data.csv', 'w', newline='', encoding='utf-8') as file:
    #     writer = csv.DictWriter(file, fieldnames=['username', 'full_name', 'bio', 'followers', 'bio_links', 'url'])
    #     writer.writeheader()
    #     writer.writerow(profile_data['user'])

    # with open('threads_data.csv', 'w', newline='', encoding='utf-8') as file:
    #     writer = csv.DictWriter(file, fieldnames=['id', 'username', 'code', 'text', 'published_on', 'has_audio', 'reply_count', 'like_count', 'image_count', 'images', 'url'])
    #     writer.writeheader()

    #     for thread in profile_data['threads']:
    #         writer.writerow(thread)
    # print("Profile Data:", profile_data)

# 运行异步任务
asyncio.run(main())