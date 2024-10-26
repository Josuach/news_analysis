import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Sample text
# text = '''
# Python is an amazing programming language. 
# It is used for web development, data analysis, artificial intelligence, 
# scientific computing, and many other areas.
# Python has a simple syntax that makes it easy to learn and use. 
# It has a large community and many libraries that help you to do your work efficiently.
# '''
# Create a word cloud
wordcloud = WordCloud(width=800, height=400,
                      background_color='white',
                      max_words=200).generate(text)

# # Save the word cloud to a file
wordcloud.to_file('/home/data/win11_data/sqlite/wordcloud.png')  # Specify the filename and format

# # Optionally, display the word cloud using matplotlib
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.title('Word Cloud Example')
# plt.show()

# # Display the word cloud using matplotlib
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.title('Word Cloud Example')

# # Save the figure to a file
# plt.savefig('/home/data/win11_data/wordcloud.png', format='png', bbox_inches='tight', dpi=300)  # Specify the filename, format, and other parameters
# plt.close()  # Close the plot to free up memory
