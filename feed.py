import yaml
import xml.etree.ElementTree as xml_tree

# Load the YAML file
with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

# Create the RSS root element
rss_element = xml_tree.Element(
    'rss',
    {
        'version': '2.0',
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
    }
)

# Create channel element
channel_element = xml_tree.SubElement(rss_element, 'channel')

link_prefix = yaml_data.get('link', '')

# Add title from YAML
xml_tree.SubElement(channel_element, 'title').text = yaml_data.get('title', 'Unknown Title')
xml_tree.SubElement(channel_element, 'format').text = yaml_data.get('format', 'MP3')
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data.get('subtitle', 'No Subtitle')
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data.get('itunes', {}).get('author', 'Unknown Author')
xml_tree.SubElement(channel_element, 'description').text = yaml_data.get('description', 'No Description')
xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data.get('image', '')}).text = yaml_data.get('itunes', {}).get('image', '')
xml_tree.SubElement(channel_element, 'language').text = yaml_data.get('language', 'en-us')
xml_tree.SubElement(channel_element, 'link').text = link_prefix

# Add category
xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data.get('category', 'General')})

# Loop through items (episodes)
for item in yaml_data.get('item', []):
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text = item.get('title', 'Untitled')
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data.get('title', 'Unknown Author')
    xml_tree.SubElement(item_element, 'description').text = item.get('description', 'No Description')
    xml_tree.SubElement(item_element, 'itunes:duration').text = item.get('duration', '00:00')
    xml_tree.SubElement(item_element, 'pubDate').text = item.get('pubDate', 'Mon, 01 Jan 2024 12:00:00 GMT')
    
    # Handle enclosure
    xml_tree.SubElement(item_element, 'enclosure', {
        'url': link_prefix + item.get('file', ''),
        'type': 'audio/mpeg',
        'length': item.get('length', '')
    })

# Write to XML file
output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)

print("✅ XML file 'podcast.xml' successfully created!")

