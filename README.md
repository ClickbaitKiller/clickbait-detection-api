# Clickbait Detection API

## API format

**/v1/detect**:
	- params: 
		- List of <ID, Title, URL>

	- response:
		- List of <ID, boolean, category>
			- boolean defines if link is clickbait or not
			- category is optional and defines the type of content

**/v1/summary**:
	- params:
		- URL of the page to summarize
