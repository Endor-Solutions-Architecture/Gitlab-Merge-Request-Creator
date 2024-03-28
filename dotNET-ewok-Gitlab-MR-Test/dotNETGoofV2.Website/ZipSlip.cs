using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Net;

namespace dotNETGoofV2.Website
{
    public class ZipSlip
    {
        public void ExtractEntry(IEnumerator<ZipArchiveEntry> entriesEnumerator, string directory)
        {
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls;
            var currentEntry = entriesEnumerator.Current;
            var filePath = Path.Combine(directory, currentEntry.FullName);
            currentEntry.ExtractToFile(filePath);
        }
    }
}
