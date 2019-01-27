//
//  ViewController.swift
//  ZTI_app
//
//  Created by Adam Linke on 28/11/2018.
//  Copyright © 2018 Adam Linke. All rights reserved.
//

import UIKit
import Alamofire

class ViewController: UIViewController {
    
    var results: [String]?

    @IBOutlet weak var questionTextField: UITextField!
    override func viewDidLoad() {
        super.viewDidLoad()
        results = []
        // Do any additional setup after loading the view, typically from a nib.
    }

    @IBAction func buttonTapped(_ sender: Any) {
        if let questionTextFieldText = questionTextField.text {
            print(questionTextFieldText)
            
            var requestData = RequestData(text: questionTextFieldText)
//            let parameters = requestData.returnAsDict()
//
//
//            print(parameters2)
//
//            Alamofire.request("http://2ac84d9d.ngrok.io/", method: .post, parameters: parameters, encoding: JSONEncoding.default)
//                .responseData { response in
//                    print(response)
//            }
            
            let parameters2 = requestData.request()
            
            let url = URL(string:"http://750357e7.ngrok.io/")
            var xmlRequest = URLRequest(url: url!)
            xmlRequest.httpBody = parameters2.data(using: String.Encoding.utf8, allowLossyConversion: true)
            xmlRequest.httpMethod = "POST"
            xmlRequest.addValue("application/xml", forHTTPHeaderField: "Content-Type")
            
            // Working with substrings test
            
            Alamofire.request(xmlRequest)
                .responseData { (response) in
                    let stringResponse: String = String(data: response.data!, encoding: String.Encoding.utf8) as String!
                    debugPrint(stringResponse)
                    
                    let result = stringResponse.dbpediaExtractor()
                    print(result)
                    self.results = result
                    
                    self.performSegue(withIdentifier: "tableViewID", sender: nil)
                    
                    // przdziel wartość i zrób reload
                    // zrób reload tableView
            }
            
        }
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        let destinationVC = segue.destination as? TableViewController
        destinationVC?.results = results
        
        //print("test2")
        print(destinationVC?.results?.count)
    }
    
    @IBAction func textFieldPressedReturn(_ sender: Any) {
        self.view.endEditing(true)
    }
    
}

extension String {
    
    func dbpediaExtractor() -> [String] {
        if let regex = try? NSRegularExpression(pattern: "dbpedia:[a-z0-9_]+", options: .caseInsensitive)
        {
            let string = self as NSString
            
            return regex.matches(in: self, options: [], range: NSRange(location: 0, length: string.length)).map {
                string.substring(with: $0.range).replacingOccurrences(of: "dbpedia:", with: "")
            }
        }
        
        return []
    }
}
