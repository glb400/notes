if ([obj isKindOfClass:[NSString class]]){

}

if ([obj respondsToSelector:@selector(shoot)]){

}

SEL shoootSelector = @selector(shoot);

[obj performSelector:shoootSelector];
[obj performSelector:shootAtSelector withObject:coordinate];
[array makeObjectsPerformSelector];

[button addTarget:self action:@selector(function:)...];


// MyProtocol.h

// 协议类似于抽象类

@protocol MyProtocol <NSObject>

@required

- (void)test1;
- (void)test2;

@optional

- (void)test3;

@end

// Person.h

@protocol MyProtocol

@interface Person : NSObject <MyProtocol>

@property (nonatomic, strong) id<MyProtocol> obj;

@property (nonatomic, strong) NSObject<MyProtocol> *nsobj;

@end


// 分类（category）是一种编译时手段，允许通过给一个类添加方法来扩充它

//NSString 表示将要添加分类的类名称，该类必须是已存在的。

//CamelCase 是为类添加的方法名称。

//只能添加方法，不能添加变量。

//头文件命名惯例:ClassName+CategoryName.h

@interface NSString (CamelCase)

- (NSString*) camelCaseString;

@end

@implementation NSString (CamelCase)

- (NSString*) camelCaseString
{
	NSString *castr = [self capitalizedString];

	NSArray *array = [castr componentsSeparatedByCharactersInSet:
						[NSCharacterSet whitespaceCharacterSet]];

	NSString *output = @"";
	for(NSString *word in array)
	{
		output = [output stringByAppendingString:word];
	}

	return output;
}

@end


// 扩展(Extension) 扩展是一种匿名分类；但是和匿名分类不一样的是，扩展可以添加新的实例变量

// ExtensionClass.h

@interface ExtensionClass : NSObject
@property (retain readonly) float value;

@end

// ExtensionClass.m

@interface ExtensionClass()
@property (retain, readwrite) float value;

- (void)privateMethod;
@end

@implementation ExtensionClass

- (void)privateMethod{

}
@end


// category 

// 不能增加实例变量

// 增强类功能

// extension

// 用于接口分离

// Block

// block是带有自动变量值的匿名函数，定义block的方法与函数类似，如

^int (int count){ return count + 1; }

// 当不用参数时参数列表可省略：

^void (void){ printf("hello");}

^{printf("hello");}

// 声明一个block类型的变量

int (^blk)(int);

// block作为方法的参数

+ (void)func:(void(^)(id))callBack;

// 将block赋值给block类型变量

int (^blk)(int) = ^int (int count) {
	return count;
}

// 用typedef为block定义别名

typedef int (^func)(int);

func a = ^(int count){
	return count;
}

// __block标识符

// Exp. 我们想在Block里面改变在Block以外的变量值

__block int a = 0;
void (^blk)(void) = ^{ a = 1;};
blk();
printf("a = %d", a);

// 在截获Objective-C对象时，如下是没有问题的，因为m就是一个对象指针，所以Block是截获了指针，在Block里面对指针所指向的内容进行修改是可以的。

NSMutableArray *m = [NSMutableArray array];
void (^blk)(void) = ^{
	[m addObject:@"abc"];
};
blk();
NSLog(@"m[0] = %@", m[0]);

// wrong code 

NSMutableArray *m = [NSMutableArray array];
void (^blk)(void) = ^{
	m = [NSMutableArray array];
}

// correct code

__block NSMutableArray *m = [NSMutableArray array];
void (^blk)(void) = ^{
	m = [NSMutableArray array];
}

// NSDictionary用block遍历

__block BOOL stoppedEarly = NO;
double stopValue = 53.5;

NSDictionary *dict = [NSDictionary dictionaryWithObjectsAndKeys:
                      @"Value1", @"Key1", @"Value2", @"Key2", @53.5, @"Key3", nil];

[dict enumerateKeysAndObjectsUsingBlock:^(id  _Nonnull key, id  _Nonnull obj, BOOL * _Nonnull stop) {
    NSLog(@"Key: %@, Value: %@", key, obj);
    if ([@"ENOUGH" isEqualToString:key]) {
        *stop = YES;
    }
    
    if ([obj doubleValue] == stopValue) {
        *stop = stoppedEarly = YES;
    }
}];

if (stoppedEarly) NSLog(@"I stopped logging dictionary value early.");