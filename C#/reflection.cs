using System;
using System.Reflection;
using System.Reflection.Emit;

// Create a class having two public methods and one protected method.
public class MyTypeClass
{
    [System.AttributeUsage(System.AttributeTargets.Class |
                           System.AttributeTargets.Struct,
                           AllowMultiple = true)  // multiuse attribute
    ]
    public class Author : System.Attribute
    {
        string name;
        public double version;

        public Author(string name)
        {
            this.name = name;
            version = 1.0;  // Default value
        }

        public string GetName()
        {
            return name;
        }
    }

    [Author("H. Ackerman")]
    private class FirstClass
    {
        // ...
    }

    // No Author attribute
    private class SecondClass
    {
        // ...
    }

    [Author("H. Ackerman"), Author("M. Knott", version = 2.0)]
    private class ThirdClass
    {
        // ...
    }

    class TestAuthorAttribute
    {
        static void Main()
        {
            PrintAuthorInfo(typeof(FirstClass));
            PrintAuthorInfo(typeof(SecondClass));
            PrintAuthorInfo(typeof(ThirdClass));
            Console.ReadKey();
        }

        private static void PrintAuthorInfo(System.Type t)
        {
            System.Console.WriteLine("Author information for {0}", t);
            System.Attribute[] attrs = System.Attribute.GetCustomAttributes(t);  // reflection

            foreach (System.Attribute attr in attrs)
            {
                if (attr is Author)
                {
                    Author a = (Author)attr;
                    System.Console.WriteLine("   {0}, version {1:f}", a.GetName(), a.version);
                }
            }
        }
    }
}