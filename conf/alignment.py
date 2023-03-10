import os
from conf.base import Base

class Alignment(Base):
    """
    Alignment configure file, which contains training parameters of alignment.
    """
    def __init__(self, work_dir="./"):
        super(Alignment, self).__init__("alignment", work_dir)
        
        self.note = ""
        
        self.net = "stackedHGnet_v1"
        self.nstack = 4
        self.loader_type = "alignment"
        self.data_definition = "300WDense" # COFW, 300W, WFLW, 300WDense, WFLWDense
        self.batch_size = 32
        self.channels = 3
        self.width = 256
        self.height = 256
        self.means = (127.5, 127.5, 127.5)
        self.scale = 1 / 127.5
        self.landmark = None
        self.aug_prob = 1.0
        
        self.display_iteration = 10
        self.val_epoch = 10
        self.model_save_epoch = 10
        #self.milestones = [100, 150, 180]
        #self.max_epoch = 200
        self.milestones = [200, 350, 450]
        self.max_epoch = 500
        
        self.optimizer = "adam"
        self.learn_rate = 0.001
        self.weight_decay = 0.00001
        self.betas = [0.9, 0.999]
        self.gamma = 0.1
        
        self.ema = True
        
        # extra
        self.add_coord = True
        self.pool_type = "origin" # origin, blur
        self.use_multiview = False
        
        # COFW
        if self.data_definition == "COFW":
            self.edge_info = (
                (True, (0, 4, 2, 5)), # RightEyebrow
                (True, (1, 6, 3, 7)), # LeftEyebrow
                (True, (8, 12, 10, 13)), # RightEye
                (False, (9, 14, 11, 15)), # LeftEye
                (True, (18, 20, 19, 21)), # Nose
                (True, (22, 26, 23, 27)), # LowerLip
                (True, (22, 24, 23, 25)), # UpperLip
            )
            #self.nme_left_index = 8 # ocular
            #self.nme_right_index = 9 # ocular
            self.nme_left_index = 16 # pupils
            self.nme_right_index = 17 # pupils
            self.classes_num = self.nstack * [29, 7, 29]
            self.crop_op = True
            self.flip_mapping = (
                [0, 1], [4, 6], [2, 3], [5, 7], [8, 9], [10, 11], [12, 14], [16, 17], [13, 15], [18, 19], [22, 23],
            )
        # 300W
        elif self.data_definition == "300W":
            self.edge_info = (
                (False, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)), # FaceContour
                (False, (17, 18, 19, 20, 21)), # RightEyebrow
                (False, (22, 23, 24, 25, 26)), # LeftEyebrow
                (False, (27, 28, 29, 30)), # NoseLine
                (False, (31, 32, 33, 34, 35)), # Nose
                (True, (36, 37, 38, 39, 40, 41)), # RightEye
                (True, (42, 43, 44, 45, 46, 47)), # LeftEye
                (True, (48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59)), # OuterLip
                (True, (60, 61, 62, 63, 64, 65, 66, 67)), # InnerLip
            )
            self.nme_left_index = 36 # ocular
            self.nme_right_index = 45 # ocular
            self.classes_num = self.nstack * [68, 9, 68]
            self.crop_op = True
            self.flip_mapping = (
                 [0, 16], [1, 15], [2, 14], [3, 13], [4, 12], [5, 11], [6, 10], [7, 9],
                 [17, 26], [18, 25], [19, 24], [20, 23], [21, 22],
                 [31, 35], [32, 34],
                 [36, 45], [37, 44], [38, 43], [39, 42], [40, 47], [41, 46],
                 [48, 54], [49, 53], [50, 52], [61, 63], [60, 64], [67, 65], [58, 56], [59, 55],
            )
        # WFLW
        elif self.data_definition == "WFLW":
            self.edge_info = (
                (False, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32)), # FaceContour
                (True, (33, 34, 35, 36, 37, 38, 39, 40, 41)), # RightEyebrow
                (True, (42, 43, 44, 45, 46, 47, 48, 49, 50)), # LeftEyebrow
                (False, (51, 52, 53, 54)), # NoseLine
                (False, (55, 56, 57, 58, 59)), # Nose
                (True, (60, 61, 62, 63, 64, 65, 66, 67)), # RightEye
                (True, (68, 69, 70, 71, 72, 73, 74, 75)), # LeftEye
                (True, (76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87)), # OuterLip
                (True, (88, 89, 90, 91, 92, 93, 94, 95)), # InnerLip
            )
            #self.nme_left_index = 96 # pupils
            #self.nme_right_index = 97 # pupils
            self.nme_left_index = 60 # ocular
            self.nme_right_index = 72 # ocular
            self.classes_num = self.nstack * [98, 9, 98]
            self.crop_op = True
            self.flip_mapping = (
                 [0, 32],  [1,  31], [2,  30], [3,  29], [4,  28], [5, 27], [6, 26], [7, 25], [8, 24], [9, 23], [10, 22],
                 [11, 21], [12, 20], [13, 19], [14, 18], [15, 17], # cheek
                 [33, 46], [34, 45], [35, 44], [36, 43], [37, 42], [38, 50], [39, 49], [40, 48], [41, 47], # elbrow
                 [60, 72], [61, 71], [62, 70], [63, 69], [64, 68], [65, 75], [66, 74], [67, 73],
                 [55, 59], [56, 58],
                 [76, 82], [77, 81], [78, 80], [87, 83], [86, 84],
                 [88, 92], [89, 91], [95, 93], [96, 97]
            )
        # dense 300W
        elif self.data_definition == "300WDense":
            self.edge_info = (
                (False, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80)), # C_1_FaceContour
                (False, (81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101)), # C_2_2_RightEyebrow
                (False, (102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122)), # C_2_1_LeftEyebrow
                (False, (123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138)), # C_4_1_NoseLine
                (False, (139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159)), # C_4_2_Nose
                (True, (160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189)), # C_3_2_RightEye
                (True, (190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219)), # C_3_1_LeftEye
                (True, (220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279)), # C_5_1_OuterLip
                (True, (280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319)), # C_5_2_InnerLip
            )
            self.nme_left_index = 160 # ocular
            self.nme_right_index = 205 # ocular
            self.classes_num = self.nstack * [320, 9, 320]
            self.crop_op = True
            self.flip_mapping = None
        # dense WFLW
        elif self.data_definition == "WFLWDense":
            self.edge_info = (
                (False, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160)), # C_1_FaceContour
                (True, (161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205)), # C_2_2_RightEyebrow
                (True, (206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250)), # C_2_1_LeftEyebrow
                (False, (251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266)), # C_4_1_NoseLine
                (False, (267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287)), # C_4_2_Nose
                (True, (288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327)), # C_3_2_RightEye
                (True, (328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367)), # C_3_1_LeftEye
                (True, (368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427)), # C_5_1_OuterLip
                (True, (428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467)), # C_5_2_InnerLip
            )
            #self.nme_left_index = 468 + 96 # pupils
            #self.nme_right_index = 468 + 97 # pupils
            self.nme_left_index = 468 + 60 # ocular
            self.nme_right_index = 468 + 72 # ocular
            self.classes_num = self.nstack * [468 + 98, 9, 468 + 98]
            self.crop_op = True
            self.flip_mapping = None
            
        self.label_num = len(self.classes_num)
        
        self.loss_lambda = 2.0
        self.loss_weights = []
        self.criterions = []
        self.metrics = []
        for i in range(self.nstack):
            factor = (2 ** i) / (2 ** (self.nstack - 1))
            self.loss_weights += [factor * weight for weight in [1.0, 10.0, 10.0]]
            self.criterions += ["AnisotropicDirectionLoss", "AWingLoss", "AWingLoss"]
            self.metrics += ["NME", None, None]
        self.key_metric_index = (self.nstack - 1) * 3
        self.use_tags = False
        
        # data
        self.train_tsv_file = os.path.join(self.data_dir, self.data_definition, "train.tsv")
        self.val_tsv_file   = os.path.join(self.data_dir, self.data_definition, "test.tsv")
        self.test_tsv_file  = os.path.join(self.data_dir, self.data_definition, "test.tsv")
        self.train_pic_dir  = os.path.join(self.data_dir, self.data_definition)
        self.val_pic_dir    = os.path.join(self.data_dir, self.data_definition)
        self.test_pic_dir   = os.path.join(self.data_dir, self.data_definition)
