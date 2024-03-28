using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using dotNetGoofV2.Website.Models;
using dotNETGoofV2.Website.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Logging;

namespace dotNETGoofV2.Website.Pages
{
    public class IndexModel : PageModel
    {
        private readonly ILogger<IndexModel> _logger;
        public JsonFileProductsService ProductService;
        public IEnumerable<Product> Products { get; private set; } //remove private?

        // Asking for a logger - built in with ASP
        public IndexModel(ILogger<IndexModel> logger,
            JsonFileProductsService productService) //Telling ASP "I need some stuff, go get it"
        {
            _logger = logger;
            ProductService = productService;
        }

        public void OnGet()
        {
            Products = ProductService.GetProducts();
        }
    }
}
