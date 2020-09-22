<p align="center">
  <img width="200px" alt="peeker-logo"
    src="docs/logo.png"
  />
</p>
<p align="center">
<a href="http://xuluhang.cn"><img src="https://travis-ci.org/GlacierSheep/DomainBlockList.svg?branch=master" alt="Build status" height="18"></a>
</p>
<h2 align="center"><code>DomainBlockList</code></h2>

## 📜 About
DomainBlockList is part of Peeker, which provides a part of the feed for Peeker. These feeds are mainly composed of domain names, and of course some IPs (we think these IPs are high-value intelligence)

## ⚒️ Start contributing
I wanted to make the setup of the environment as easy as possible. To start the environment you need the 
following prerequisites:

### Prerequisites
  * GitPython
  * loguru
  * pandas
  * pyfiglet
  * requests
  * termcolor
  
### Start environment
You only (_fingers crossed_) need to execute the following to start the environment:

```commandline
pip install -r requirements.txt
```

## Architecture and patterns

The structure of the code is the following:
  * `DomainBlockList/craw`: the main code is kept here.
  * `DomainBlockList/trail`: trail files are kept here.
  * `DomainBlockList/Log`: log files
    
## FAQ
**What can these trails be used for?**

 * They can be integrated into the firewall as rules.
 * They can be used for data mining, for example as the Feed of Peeker.

**How often is the data updated?**

 * Update data every 6 hours
 
## 🚩 License
The code is available under the [MIT license](LICENSE.md).
