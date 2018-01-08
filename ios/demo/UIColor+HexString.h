//
//  UIColor+HexString.h
//  demo
//
//  Created by jrm on 8/15/17.
//  Copyright © 2017 frmdstryr. All rights reserved.
//

#ifndef UIColor_HexString_h
#define UIColor_HexString_h

#import <UIKit/UIKit.h>


@interface UIColor(HexString)

+ (UIColor *) colorWithHexString: (NSString *) hexString;

@end


#endif /* UIColor_HexString_h */
