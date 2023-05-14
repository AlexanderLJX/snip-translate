import { translate } from '@vitalets/google-translate-api';
import fs from 'fs';
import { HttpProxyAgent } from 'http-proxy-agent';

const inputFile = process.argv[2];
const outputFile = process.argv[3];
const proxyTimeout = parseInt(process.argv[4]);
const proxyListFile = 'proxies.txt';
const workingProxyFile = 'workingProxy.txt';

fs.readFile(proxyListFile, 'utf8', async (err, proxies) => {
  if (err) {
    console.error(err);
    process.exit(1);
  }

  const proxyArray = proxies.split('\n');

  async function translateWithProxy(data, proxy) {
    console.log(`Using proxy: ${proxy}`);
    const agent = new HttpProxyAgent(`http://${proxy}`);
  
    try {
      const { text: translatedText } = await Promise.race([
        translate(data, { to: 'en', fetchOptions: { agent } }),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Proxy request timeout')), proxyTimeout)
        ),
      ]);
  
      fs.writeFile(outputFile, translatedText, (err) => {
        if (err) {
          console.error(err);
          process.exit(1);
        }
        console.log('Translation succeeded and text has been written to the output file');
        process.exit();
      });
      return true;
    } catch (e) {
      if (e.name === 'TooManyRequestsError') {
        console.log('Too many requests, try again with another proxy');
        return false;
      } else if (e.message === 'Proxy request timeout') {
        console.log('Proxy request timed out, trying another proxy');
        return false;
      } else {
        console.error(e);
        return false;
      }
    }
  }
  

  fs.readFile(inputFile, 'utf8', async (err, data) => {
    if (err) {
      console.error(err);
      process.exit(1);
    }

    let success = false;
    let proxy;

    // First, try the working proxy if it exists
    if (fs.existsSync(workingProxyFile)) {
      proxy = fs.readFileSync(workingProxyFile, 'utf8');
      success = await translateWithProxy(data, proxy);
    }

    // If the working proxy failed or didn't exist, try the other proxies
    if (!success) {
      if (proxy) {
        // Remove the failed working proxy from the file
        fs.unlinkSync(workingProxyFile);
        // Remove the failed proxy from the list
        proxyArray.splice(proxyArray.indexOf(proxy), 1);
      }

      const promises = proxyArray.map(async (proxy) => {
        const result = await translateWithProxy(data, proxy);
        if (result) {
          // Save the working proxy for future runs
          fs.writeFileSync(workingProxyFile, proxy);
        }
        return result;
      });
      
      const results = await Promise.all(promises);
      success = results.some((result) => result);
    }

    if (success) {
      console.log('Translation succeeded with at least one proxy.');
    } else {
      console.error('Failed to translate with all available proxies');
      process.exit(1);
    }
  });
});
