using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using dotNetGoofV2.Website.Models;
using Microsoft.AspNetCore.Hosting;

namespace dotNETGoofV2.Website.Services
{
    public class JsonFileProductsService
    {
        public JsonFileProductsService(IWebHostEnvironment webHostEnvironment)
        {
            WebHostEnvironment = webHostEnvironment;
        }

        public IWebHostEnvironment WebHostEnvironment { get; }

        private string JsonFileName
        {
            // webroot path = wwwroot
            // Maybe hard code the file path to show maybe zip slip? 
            get { return Path.Combine(WebHostEnvironment.WebRootPath, "data", "goof-data.json"); }
        }

        public IEnumerable<Product> GetProducts()
        {
            using (var jsonFileReader = File.OpenText(JsonFileName))
            {
                return JsonSerializer.Deserialize<Product[]>(jsonFileReader.ReadToEnd(),
                    new JsonSerializerOptions
                    {
                        PropertyNameCaseInsensitive = true
                    });
            }
        }

        public void AddRating(string productId, int rating)
        {
            var products = GetProducts();
            //LINQ
            //This is the correct way:
            var enumerable = products as Product[] ?? products.ToArray();
            var query = enumerable.First(x => x.Id == productId);
            //Need to add a SQL injection vuln of the above statement
            if (query.Ratings == null)
            {
                query.Ratings = new int[] { rating };
            }
            else
            {
                var ratings = query.Ratings.ToList();
                ratings.Add(rating);
                query.Ratings = ratings.ToArray();
            }

            using (var outputStream = File.OpenWrite(JsonFileName))
            {
                JsonSerializer.Serialize<IEnumerable<Product>>(
                    new Utf8JsonWriter(outputStream, new JsonWriterOptions
                    {
                        SkipValidation = true,
                        Indented = true
                    }),
                    enumerable
                );
            }
        }
    }
}
