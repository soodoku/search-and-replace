### (Turbo) Search and Replace 

## What It Does:

1. Removes extra blank lines
2. Searches and replaces words 
	a. takes replacelist.csv that carries word pairs (original_word,replace_with_this_word) 
	b. open in a unicode editor like Notepad++.
3. Regex
	Allows for 0-X consecutive errors within a word.
	Takes wordlist.csv that carries words and X for each word
	For instance if a row in wordlist.csv reads: Available,1
	Av.{0,1}\??[\r\n]*ilable ==> Available
	Ava.{0,1}\??[\r\n]*lable ==> Available
4.  Removes soft-hyphens followed by new line (this typically means multi-line words)


# Running the script 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<pre><code>
Usage: postprocess_r4.py [options] <source text directory>

Options:
  -h, --help            show this help message and exit
  -o OUTDIR, --outdir=OUTDIR
                        Text output directory (default: postprocessed)
  -r, --resume          Resume postprocessing (Skip if existing) (default:
                        False)

USAGE EXAMPLE :-
    python postprocess_r2.py txt_dir

</code></pre>	
The script will be post process all text files in 'text' directory and save
the output file to the 'postprocessed' directory
