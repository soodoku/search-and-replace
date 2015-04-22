### Turbo Search and Replace 

The script does the following:  

1. Removes extra blank lines.  
2. Removes soft-hyphens followed by new line (this typically means multi-line words).  
3. Searches and replaces a list of words:   
   The script takes a csv (replacelist.csv) that carries words to be replaced, and replacement words.  
4. Regular expression based replacement: 
   * Allows for 0-X consecutive errors within a word.  
   * Takes wordlist.csv that carries words and X for each word    
   * For instance if a row in wordlist.csv reads: Available,1    
   * Av.{0,1}\??[\r\n]*ilable ==> Available    
   * Ava.{0,1}\??[\r\n]*lable ==> Available 

#### Running the script 

The script looks for two files:  
1. replacelist.csv -- carries word pairs (original_word, replace_with_this_word). Here's a sample [replacelist.csv](https://github.com/soodoku/Search-And-Replace/blob/master/replacelist.csv)  
2. wordlist.csv -- carries the correct word, and number of consecutive errors tolerated. All the variously misspelled words will be replaced with the correct word. Here's a sample [wordlist.csv](https://github.com/soodoku/Search-And-Replace/blob/master/wordlist.csv)  

<pre><code>
Usage: postprocess.py [options] source_txt_directory

Options:
  -h, --help            show this help message and exit
  -o OUTDIR, --outdir=OUTDIR
                        Text output directory (default: postprocessed)
  -r, --resume          Resume postprocessing (Skip if existing) (default:
                        False)

EXAMPLE:
    python postprocess.py txt_dir
</code></pre>	

The script will be post process all text files in 'text' directory and save the output file to the 'postprocessed' directory.

#### License

Scripts are released under the [MIT License](https://github.com/soodoku/Search-And-Replace/blob/master/License.md).
